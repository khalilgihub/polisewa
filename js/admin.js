/**
 * PoliSewa - Admin Console & Moderation Module (js/admin.js)
 * Manages admin statistics, property listing verification, moderation, and pin location.
 */

var adminPropertiesData = [];

// 1. Open / Close Admin Modal
function openAdminDashboardModal() {
    if (!currentUser || currentUser.role !== 'admin') return;
    var authDropdown = document.getElementById('auth-dropdown');
    var adminModalOverlay = document.getElementById('admin-modal-overlay');
    if (authDropdown) authDropdown.classList.remove('active');
    if (adminModalOverlay) adminModalOverlay.classList.add('active');
    loadAdminData();
}

function closeAdminDashboardModal() {
    var adminModalOverlay = document.getElementById('admin-modal-overlay');
    if (adminModalOverlay) adminModalOverlay.classList.remove('active');
}

document.addEventListener('DOMContentLoaded', function () {
    var adminModalOverlay = document.getElementById('admin-modal-overlay');
    if (adminModalOverlay) {
        adminModalOverlay.onclick = function (e) {
            if (e.target === adminModalOverlay) {
                closeAdminDashboardModal();
            }
        };
    }
});

// 2. Load Admin Data (Stats & Properties)
function loadAdminData() {
    if (!currentUser || currentUser.role !== 'admin') return;

    // 1. Fetch Stats
    fetch('/api/admin/stats?admin_id=' + encodeURIComponent(currentUser.id) + '&admin_email=' + encodeURIComponent(currentUser.email || ''))
        .then(function (res) { return res.json(); })
        .then(function (stats) {
            if (stats && !stats.error) {
                var statProp = document.getElementById('admin-stat-properties');
                var statVer = document.getElementById('admin-stat-verified');
                if (statProp) statProp.innerText = stats.totalProperties || 0;
                if (statVer) statVer.innerText = stats.verifiedProperties || 0;
            }
        })
        .catch(function (e) { console.error('Stats error:', e); });

    // 2. Fetch Properties for Moderation
    fetch('/api/properties?user_id=' + encodeURIComponent(currentUser.id))
        .then(function (res) { return res.json(); })
        .then(function (props) {
            adminPropertiesData = Array.isArray(props) ? props : [];
            filterAdminProperties();
        })
        .catch(function (e) { console.error('Props error:', e); });
}

// 3. Properties Filtering & Table Rendering
function filterAdminProperties() {
    var searchInput = document.getElementById('admin-prop-search');
    var filterInput = document.getElementById('admin-prop-filter');
    var search = searchInput ? searchInput.value.toLowerCase().trim() : '';
    var statusFilter = filterInput ? filterInput.value : 'all';

    var filtered = adminPropertiesData.filter(function (p) {
        var matchesSearch = !search ||
            (p.name && p.name.toLowerCase().includes(search)) ||
            (p.landlord_name && p.landlord_name.toLowerCase().includes(search)) ||
            (p.phone && p.phone.includes(search));

        var matchesStatus = true;
        if (statusFilter === 'verified') matchesStatus = p.is_verified === 1;
        else if (statusFilter === 'unverified') matchesStatus = !p.is_verified || p.is_verified === 0;

        return matchesSearch && matchesStatus;
    });

    renderAdminPropertiesTable(filtered);
}

function renderAdminPropertiesTable(list) {
    var tbody = document.getElementById('admin-properties-tbody');
    if (!tbody) return;

    if (list.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="admin-table-empty">No property listings found.</td></tr>';
        return;
    }

    var html = '';
    list.forEach(function (p) {
        var imgUrls = (typeof parseImageUrls === 'function') ? parseImageUrls(p.image) : [];
        var thumb = imgUrls[0] || 'https://placehold.co/80x60?text=No+Photo';
        var isVer = p.is_verified === 1;

        var dObj = (typeof parsePropertyDetails === 'function') ? parsePropertyDetails(p.details) : null;
        var specSnippet = '';
        if (dObj) {
            var parts = [];
            if (dObj.room_type) parts.push('🛏️ ' + dObj.room_type);
            if (dObj.bathroom_type) parts.push('🚿 ' + dObj.bathroom_type);
            if (dObj.floor_level && Array.isArray(dObj.floor_level) && dObj.floor_level.length > 0) parts.push('🏢 ' + dObj.floor_level[0] + ' Flr');
            if (parts.length > 0) {
                specSnippet = '<div style="font-size:11px;color:#2563eb;font-weight:600;margin-top:3px;">' + escapeHtml(parts.join(' • ')) + '</div>';
            }
        }

        html += '<tr>' +
            '<td>' +
            '<div class="admin-prop-cell">' +
            '<img src="' + escapeHtml(thumb) + '" class="admin-table-thumb" alt="thumb" onerror="this.src=\'https://placehold.co/80x60?text=Photo\'" />' +
            '<div>' +
            '<div class="admin-prop-name">' + escapeHtml(p.name || 'Unnamed Property') + '</div>' +
            '<div class="admin-prop-desc">' + escapeHtml(p.desc ? (p.desc.substring(0, 45) + '...') : '') + '</div>' +
            specSnippet +
            '</div>' +
            '</div>' +
            '</td>' +
            '<td>' +
            '<div class="admin-user-cell">' +
            '<span class="admin-user-name">' + escapeHtml(p.landlord_name || 'Landlord') + '</span>' +
            '<span class="admin-user-sub">' + escapeHtml(p.phone || '-') + '</span>' +
            '</div>' +
            '</td>' +
            '<td><span class="admin-price-badge">RM ' + escapeHtml(p.price || '0') + '/mo</span></td>' +
            '<td>' +
            '<button class="admin-status-toggle ' + (isVer ? 'status-verified' : 'status-unverified') + '" onclick="adminTogglePropertyVerify(' + p.id + ', ' + (isVer ? 1 : 0) + ')" title="' + (isVer ? 'Click to hide from map' : 'Click to approve and publish') + '">' +
            (isVer ? '✓ Approved' : '⏳ Pending') +
            '</button>' +
            '</td>' +
            '<td style="text-align:right;">' +
            '<div class="admin-action-btns">' +
            '<button class="admin-tbl-btn admin-tbl-locate" title="Locate on Map" onclick="adminLocateProperty(' + p.lat + ', ' + p.lng + ', ' + p.id + ')">📍 Map</button>' +
            '<button class="admin-tbl-btn admin-tbl-delete" title="Delete Listing" onclick="adminDeleteProperty(' + p.id + ', \'' + escapeHtml(p.name).replace(/'/g, "\\'") + '\')">🗑️</button>' +
            '</div>' +
            '</td>' +
            '</tr>';
    });
    tbody.innerHTML = html;
}

// 4. Admin Actions (Approve/Unapprove Listing, Delete Listing, Locate Pin)
function adminTogglePropertyVerify(propId, currentStatus) {
    var newStatus = currentStatus === 1 ? 0 : 1;
    fetch('/api/properties/' + propId + '/verify', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ admin_id: currentUser.id, admin_email: currentUser.email, is_verified: newStatus })
    })
        .then(function (res) { return res.json().then(function (d) { if (!res.ok) throw new Error(d.error); return d; }); })
        .then(function () {
            if (typeof loadProperties === 'function') loadProperties();
            loadAdminData();
        })
        .catch(function (err) { alert('Error: ' + err.message); });
}

function adminDeleteProperty(propId, propName) {
    if (!confirm('Are you sure you want to delete "' + propName + '"? All property photos will also be permanently deleted.')) return;

    fetch('/api/properties/' + propId + '?user_id=' + currentUser.id + '&admin_email=' + encodeURIComponent(currentUser.email || ''), {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: currentUser.id, admin_email: currentUser.email })
    })
        .then(function (res) { return res.json().then(function (d) { if (!res.ok) throw new Error(d.error); return d; }); })
        .then(function () {
            if (typeof loadProperties === 'function') loadProperties();
            loadAdminData();
        })
        .catch(function (err) { alert('Error: ' + err.message); });
}

function adminLocateProperty(lat, lng, propId) {
    closeAdminDashboardModal();
    map.flyTo([lat, lng], 17, { animate: true, duration: 1.0 });
    setTimeout(function () {
        var found = (landlordMarkers || []).find(function (m) { return m.id === propId; });
        if (found && found.marker) {
            found.marker.openPopup();
        }
    }, 600);
}
