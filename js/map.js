/**
 * PoliSewa - Map & Marker Management Module (js/map.js)
 * Manages Leaflet map instance, Kuching boundary polygon, markers & popup cards.
 */

// Define geographic bounds for Kuching region (Lat 1.15..1.85, Lng 109.80..110.70)
var kuchingMaxBounds = L.latLngBounds(
    L.latLng(1.15, 109.80),
    L.latLng(1.85, 110.70)
);

// 1. Initialize Leaflet Map centered on Kuching
var map = L.map('map', {
    zoomControl: false,
    attributionControl: false,
    maxBounds: kuchingMaxBounds,
    maxBoundsViscosity: 1.0,
    minZoom: 11,
    maxZoom: 19,
    tap: true
}).setView([1.5535, 110.3593], 13);

// 2. Add Base Map Tiles
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

// 3. Boundary check for Kuching region
function isInsideKuchingBoundary(lat, lng) {
    return kuchingMaxBounds.contains([lat, lng]);
}

// 4. Special Marker: Politeknik Kuching Sarawak
var polytechnicLatLng = [1.630688, 110.193062];
var polytechIcon = L.divIcon({
    className: 'custom-div-icon',
    html: '<div class="marker-pin"></div><span>🎓</span>',
    iconSize: [30, 30],
    iconAnchor: [15, 30],
    popupAnchor: [0, -30]
});
var polytechMarker = L.marker(polytechnicLatLng, { icon: polytechIcon }).addTo(map);
polytechMarker.bindPopup("<b>Politeknik Kuching Sarawak (PKS)</b><br>Batu 8, Jalan Matang");

polytechMarker.on('click', function (e) {
    map.flyTo(e.latlng, 16, { animate: true, duration: 0.8 });
});

var jumpPksBtn = document.getElementById('btn-jump-pks');
if (jumpPksBtn) {
    jumpPksBtn.onclick = function () {
        map.flyTo(polytechnicLatLng, 16, { animate: true, duration: 1.0 });
        polytechMarker.openPopup();
    };
}

// 5. Landlord Property Markers State
var landlordMarkers = [];
var pendingMarker = null;
var pendingLatLng = null;

// Phone contact link helpers
function getWhatsappUrl(phoneStr) {
    if (!phoneStr) return '#';
    var digits = phoneStr.replace(/\D/g, '');
    if (!digits) return '#';
    if (digits.startsWith('0')) {
        digits = '60' + digits.substring(1);
    } else if (!digits.startsWith('60') && (digits.length === 9 || digits.length === 10)) {
        digits = '60' + digits;
    }
    return 'https://wa.me/' + digits;
}

function getCallUrl(phoneStr) {
    if (!phoneStr) return '#';
    var cleanPhone = phoneStr.trim().replace(/[^0-9+]/g, '');
    return 'tel:' + cleanPhone;
}

function buildContactButtonsHtml(phoneStr) {
    if (!phoneStr) return '';
    var waUrl = getWhatsappUrl(phoneStr);
    var callUrl = getCallUrl(phoneStr);

    return '<div class="contact-actions">' +
        '<a href="' + waUrl + '" target="_blank" rel="noopener" class="contact-btn contact-btn-wa" title="Chat on WhatsApp">' +
            '<svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor" style="flex-shrink:0;"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.888 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>' +
            '<span>WhatsApp</span>' +
        '</a>' +
        '<a href="' + callUrl + '" class="contact-btn contact-btn-call" title="Call Landlord">' +
            '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>' +
            '<span>Direct Call</span>' +
        '</a>' +
    '</div>';
}

// Utility to parse single image string, JSON array, or comma-separated string
function parseImageUrls(imageVal) {
    if (!imageVal) return [];
    if (Array.isArray(imageVal)) return imageVal.filter(Boolean);
    if (typeof imageVal === 'string') {
        var trimmed = imageVal.trim();
        if (trimmed.startsWith('[')) {
            try {
                var parsed = JSON.parse(trimmed);
                if (Array.isArray(parsed)) return parsed.filter(Boolean);
            } catch (e) {}
        }
        if (trimmed.includes(',')) {
            return trimmed.split(',').map(function(s) { return s.trim(); }).filter(Boolean);
        }
        return [trimmed];
    }
    return [];
}

// Build HTML for Photo Gallery Carousel with Touch Swiping support
function buildGalleryHtml(imageUrls, galleryId, isPopup) {
    if (!imageUrls || imageUrls.length === 0) {
        return '<div class="property-gallery-container ' + (isPopup ? 'popup-gallery-container' : '') + '" style="background:#f1f5f9;display:flex;align-items:center;justify-content:center;color:#94a3b8;font-size:13px;font-weight:500;">' +
            '<div style="text-align:center;">📷<br>No photos uploaded</div>' +
            '</div>';
    }
    if (imageUrls.length === 1) {
        return '<div class="property-gallery-container ' + (isPopup ? 'popup-gallery-container' : '') + '">' +
            '<img class="gallery-slide-img" src="' + imageUrls[0] + '" alt="Property photo" loading="lazy" />' +
            '</div>';
    }

    var escapedUrls = JSON.stringify(imageUrls).replace(/"/g, '&quot;');
    var dotsHtml = '';
    for (var i = 0; i < imageUrls.length; i++) {
        dotsHtml += '<span class="gallery-dot ' + (i === 0 ? 'active' : '') + '" onclick="event.stopPropagation(); window.setGallerySlide(\'' + galleryId + '\', ' + i + ', ' + imageUrls.length + ')"></span>';
    }

    setTimeout(function() {
        enableGallerySwipe(galleryId);
    }, 50);

    return '<div id="' + galleryId + '" class="property-gallery-container ' + (isPopup ? 'popup-gallery-container' : '') + '" data-index="0" data-total="' + imageUrls.length + '" data-urls="' + escapedUrls + '">' +
        '<img class="gallery-slide-img" src="' + imageUrls[0] + '" alt="Property photo 1" />' +
        '<button type="button" class="gallery-nav-btn prev" onclick="event.stopPropagation(); window.cycleGallery(\'' + galleryId + '\', -1, ' + imageUrls.length + ')" title="Previous photo" aria-label="Previous photo">❮</button>' +
        '<button type="button" class="gallery-nav-btn next" onclick="event.stopPropagation(); window.cycleGallery(\'' + galleryId + '\', 1, ' + imageUrls.length + ')" title="Next photo" aria-label="Next photo">❯</button>' +
        '<span class="gallery-counter">1 / ' + imageUrls.length + '</span>' +
        '<div class="gallery-dots">' + dotsHtml + '</div>' +
        '</div>';
}

window.cycleGallery = function(galleryId, delta, total) {
    var container = document.getElementById(galleryId);
    if (!container) return;
    var currentIdx = parseInt(container.getAttribute('data-index') || '0', 10);
    var newIdx = (currentIdx + delta + total) % total;
    window.setGallerySlide(galleryId, newIdx, total);
};

window.setGallerySlide = function(galleryId, targetIndex, total) {
    var container = document.getElementById(galleryId);
    if (!container) return;
    var urlsStr = container.getAttribute('data-urls') || '[]';
    var urls = [];
    try { urls = JSON.parse(urlsStr); } catch (e) {}

    container.setAttribute('data-index', targetIndex);
    var img = container.querySelector('.gallery-slide-img');
    if (img && urls[targetIndex]) {
        img.style.opacity = '0.3';
        setTimeout(function() {
            img.src = urls[targetIndex];
            img.style.opacity = '1';
        }, 80);
    }
    var counter = container.querySelector('.gallery-counter');
    if (counter) {
        counter.innerText = (targetIndex + 1) + ' / ' + total;
    }
    var dots = container.querySelectorAll('.gallery-dot');
    for (var i = 0; i < dots.length; i++) {
        if (i === targetIndex) dots[i].classList.add('active');
        else dots[i].classList.remove('active');
    }
};

function enableGallerySwipe(galleryId) {
    var el = document.getElementById(galleryId);
    if (!el || el._swipeEnabled) return;
    el._swipeEnabled = true;

    var touchStartX = 0;
    var touchEndX = 0;

    el.addEventListener('touchstart', function(e) {
        touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    el.addEventListener('touchend', function(e) {
        touchEndX = e.changedTouches[0].screenX;
        var total = parseInt(el.getAttribute('data-total') || '0', 10);
        if (total > 1) {
            var diff = touchStartX - touchEndX;
            if (diff > 35) {
                window.cycleGallery(galleryId, 1, total);
            } else if (diff < -35) {
                window.cycleGallery(galleryId, -1, total);
            }
        }
    }, { passive: true });
}

// 6. Marker Popups & Details Preview
window.togglePopupFeatures = function(index, btn, event) {
    if (event) {
        event.stopPropagation();
        event.preventDefault();
    }
    var featuresRow = document.getElementById('popup-features-' + index);
    if (!featuresRow) return;

    var isHidden = featuresRow.style.display === 'none' || featuresRow.style.display === '';
    if (isHidden) {
        featuresRow.style.display = 'flex';
        if (btn) {
            btn.classList.add('active');
            btn.innerHTML = "<span class='reveal-dots-icon' style='letter-spacing:0;'>▲</span> <span class='reveal-btn-label'>Hide Room Info</span>";
        }
    } else {
        featuresRow.style.display = 'none';
        if (btn) {
            btn.classList.remove('active');
            btn.innerHTML = "<span class='reveal-dots-icon'>••••</span> <span class='reveal-btn-label'>Reveal Room Info</span>";
        }
    }

    var item = landlordMarkers[index];
    if (item && item.marker && item.marker.getPopup()) {
        item.marker.getPopup().update();
    }
};

function createMarkerPopup(index) {
    var data = landlordMarkers[index];
    if (!data) return document.createElement('div');
    var isOwner = currentUser && currentUser.id === data.user_id;
    var isAdmin = currentUser && currentUser.role === 'admin';
    var isVerified = data.is_verified === 1;

    var popupContent = document.createElement('div');
    popupContent.style.minWidth = '230px';

    var verifiedBadgeHtml = isVerified
        ? "<svg class='verified-seal-icon' width='18' height='18' viewBox='0 0 24 24' fill='none' title='Polisewa Approved'><path fill='#10B981' d='M12 1L15.39 4.39L20.18 4.39L20.18 9.18L23.57 12.57L20.18 15.96L20.18 20.75L15.39 20.75L12 24.14L8.61 20.75L3.82 20.75L3.82 15.96L0.43 12.57L3.82 9.18L3.82 4.39L8.61 4.39L12 1Z'/><path stroke='#ffffff' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round' d='M8.5 12.5L11 15L16.5 9.5'/></svg>"
        : "";

    var actionsHtml = '';
    if (isAdmin) {
        var statusHtml = isVerified
            ? "<span style='display:inline-block;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:700;background:#ecfdf5;color:#059669;border:1px solid #a7f3d0;'>✅ Approved & Live</span>"
            : "<span style='display:inline-block;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:700;background:#fef3c7;color:#d97706;border:1px solid #fde68a;'>⏳ Pending Approval</span>";

        actionsHtml = "<div style='margin-top:10px;display:flex;flex-direction:column;gap:6px;'>" +
            "<div style='display:flex;align-items:center;justify-content:space-between;padding:2px 0;'>" +
                "<span style='font-size:11.5px;color:#64748b;font-weight:600;'>Visibility:</span>" +
                statusHtml +
            "</div>" +
            "<button class='admin-verify-btn " + (isVerified ? "btn-unverify" : "btn-verify") + "' id='popup-verify-btn-" + data.id + "'>" +
                (isVerified ? "✕ Hide from Map (Unapprove)" : "✓ Approve & Publish Pin") +
            "</button>" +
            "<div style='display:flex;gap:6px;'>" +
                "<button class='edit-pin-btn' style='flex:1;padding:6px 10px;font-size:11.5px;font-weight:600;cursor:pointer;background:#2563eb;color:white;border:none;border-radius:8px;'>Edit</button>" +
                "<button class='view-pin-btn' style='flex:1;padding:6px 10px;font-size:11.5px;font-weight:600;cursor:pointer;background:#f1f5f9;color:#334155;border:1px solid #cbd5e1;border-radius:8px;'>Details</button>" +
                "<button class='remove-pin-btn' style='padding:6px 10px;font-size:11.5px;font-weight:600;cursor:pointer;background:#fee2e2;color:#ef4444;border:none;border-radius:8px;'>Delete</button>" +
            "</div>" +
            "</div>";
    } else if (isOwner) {
        var pendingNotice = !isVerified
            ? "<div style='background:#fffbeb;color:#b45309;padding:6px 9px;border-radius:8px;font-size:11px;font-weight:600;margin-top:6px;border:1px solid #fde68a;line-height:1.35;'>" +
                "⏳ <b>Pending Admin Approval</b>" +
                "<div style='font-size:10px;font-weight:400;color:#92400e;margin-top:2px;'>Visible only to you until approved by admin.</div>" +
              "</div>"
            : "";

        actionsHtml = pendingNotice +
            "<div style='margin-top:10px;display:flex;gap:8px;'>" +
                "<button class='edit-pin-btn' style='flex:1;padding:8px 12px;font-size:12px;font-weight:600;cursor:pointer;background:#2563eb;color:white;border:none;border-radius:8px;box-shadow:0 2px 6px rgba(37,99,235,0.3);'>Edit Listing</button>" +
                "<button class='remove-pin-btn' style='padding:8px 12px;font-size:12px;font-weight:600;cursor:pointer;background:#fee2e2;color:#ef4444;border:none;border-radius:8px;'>Delete</button>" +
            "</div>";
    } else {
        actionsHtml = "<div style='margin-top:10px;display:flex;align-items:center;justify-content:space-between;gap:6px;'>" +
            "<button class='view-pin-btn' style='padding:8px 14px;font-size:12px;font-weight:600;cursor:pointer;background:#2563eb;color:white;border:none;border-radius:8px;'>View Details</button>";
        if (data.landlord_name) {
            actionsHtml += "<small style='color:#64748b;font-weight:500;'>" + escapeHtml(data.landlord_name) + "</small>";
        }
        actionsHtml += "</div>";
    }

    var imageUrls = parseImageUrls(data.image);
    var imageHtml = buildGalleryHtml(imageUrls, 'popup-gallery-' + index, true);

    var detailsObj = (typeof parsePropertyDetails === 'function') ? parsePropertyDetails(data.details) : null;
    var detailsBadgesHtml = '';
    if (detailsObj) {
        var pills = [];
        if (detailsObj.room_type) {
            pills.push("<span class='popup-feature-pill pill-room'>🛏️ " + escapeHtml(detailsObj.room_type) + "</span>");
        }
        if (detailsObj.bathroom_type) {
            pills.push("<span class='popup-feature-pill pill-bath'>🚿 " + escapeHtml(detailsObj.bathroom_type) + " Bath</span>");
        }
        if (detailsObj.floor_level && Array.isArray(detailsObj.floor_level) && detailsObj.floor_level.length > 0) {
            pills.push("<span class='popup-feature-pill'>🏢 " + escapeHtml(detailsObj.floor_level.join('/')) + " Flr</span>");
        }
        if (detailsObj.utilities && Array.isArray(detailsObj.utilities) && detailsObj.utilities.length > 0) {
            var maxUtils = 3;
            for (var u = 0; u < Math.min(detailsObj.utilities.length, maxUtils); u++) {
                var uName = detailsObj.utilities[u];
                var shortU = uName.replace(' / Internet Access', '').replace('Air-Conditioning', 'Air-Con');
                var uIcon = (uName.indexOf('Air') !== -1 ? '❄️ ' : (uName.indexOf('Wifi') !== -1 ? '📶 ' : (uName.indexOf('Wash') !== -1 ? '🧺 ' : '✓ ')));
                pills.push("<span class='popup-feature-pill pill-util'>" + uIcon + escapeHtml(shortU) + "</span>");
            }
            if (detailsObj.utilities.length > maxUtils) {
                pills.push("<span class='popup-feature-pill pill-util'>+" + (detailsObj.utilities.length - maxUtils) + " more</span>");
            }
        }
        if (detailsObj.preferences && detailsObj.preferences.general && Array.isArray(detailsObj.preferences.general) && detailsObj.preferences.general.length > 0) {
            for (var g = 0; g < Math.min(detailsObj.preferences.general.length, 3); g++) {
                var genPref = detailsObj.preferences.general[g].replace('Prefer ', '').replace('Preferred ', '');
                var prefIcon = (genPref.indexOf('Deposit') !== -1 ? '💰 ' : (genPref.indexOf('move-in') !== -1 ? '🚀 ' : (genPref.indexOf('pet') !== -1 ? '🐾 ' : (genPref.indexOf('muslim') !== -1 ? '🕌 ' : '⭐ '))));
                pills.push("<span class='popup-feature-pill pill-pref'>" + prefIcon + escapeHtml(genPref) + "</span>");
            }
        }
        if (detailsObj.preferences && detailsObj.preferences.race && Array.isArray(detailsObj.preferences.race) && detailsObj.preferences.race.length > 0) {
            for (var r = 0; r < Math.min(detailsObj.preferences.race.length, 2); r++) {
                pills.push("<span class='popup-feature-pill pill-pref'>👤 " + escapeHtml(detailsObj.preferences.race[r]) + "</span>");
            }
        }
        if (detailsObj.preferences && detailsObj.preferences.occupation && Array.isArray(detailsObj.preferences.occupation) && detailsObj.preferences.occupation.length > 0) {
            for (var o = 0; o < Math.min(detailsObj.preferences.occupation.length, 2); o++) {
                pills.push("<span class='popup-feature-pill pill-pref'>💼 " + escapeHtml(detailsObj.preferences.occupation[o]) + "</span>");
            }
        }
        if (pills.length > 0) {
            detailsBadgesHtml = 
                "<div class='popup-reveal-row'>" +
                    "<button type='button' class='popup-reveal-btn' onclick='togglePopupFeatures(" + index + ", this, event)' title='Click .... to reveal room information'>" +
                        "<span class='reveal-dots-icon'>••••</span> <span class='reveal-btn-label'>Reveal Room Info</span>" +
                    "</button>" +
                "</div>" +
                "<div class='popup-features-row' id='popup-features-" + index + "' style='display:none;'>" +
                    pills.join('') +
                "</div>";
        }
    }

    popupContent.innerHTML = imageHtml +
        "<div class='popup-title-row'>" +
            "<span class='popup-prop-name'>" + escapeHtml(data.name || 'Property') + "</span>" +
            verifiedBadgeHtml +
        "</div>" +
        (data.desc ? "<div style='font-size:12px;color:#64748b;margin-bottom:6px;line-height:1.4;'>" + escapeHtml(data.desc) + "</div>" : "") +
        (data.price ? "<div style='color:#2563eb;font-weight:700;font-size:15px;margin-bottom:6px;'>RM " + escapeHtml(data.price) + "<span style='font-size:11px;font-weight:400;color:#64748b;'> /month</span></div>" : "") +
        detailsBadgesHtml +
        (data.phone ? buildContactButtonsHtml(data.phone) : "") +
        actionsHtml;

    var verifyBtn = popupContent.querySelector('.admin-verify-btn');
    if (verifyBtn) {
        verifyBtn.onclick = function(e) {
            e.stopPropagation();
            togglePropertyVerification(data.id, index, verifyBtn);
        };
    }
    var editBtn = popupContent.querySelector('.edit-pin-btn');
    if (editBtn) {
        editBtn.onclick = function(e) {
            e.stopPropagation();
            if (typeof openPropertyPanel === 'function') openPropertyPanel('edit', index);
        };
    }
    var removeBtn = popupContent.querySelector('.remove-pin-btn');
    if (removeBtn) {
        removeBtn.onclick = function(e) {
            e.stopPropagation();
            if (confirm('Delete this property listing?')) {
                fetch('/api/properties/' + data.id + '?user_id=' + currentUser.id, {
                    method: 'DELETE',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ user_id: currentUser.id })
                })
                .then(function(res) { return res.json(); })
                .then(function(result) {
                    if (result.error) {
                        alert(result.error);
                        return;
                    }
                    map.removeLayer(data.marker);
                    landlordMarkers.splice(index, 1);
                    if (typeof editingMarkerIndex !== 'undefined') editingMarkerIndex = -1;
                    rebuildAllPopups();
                    if (document.getElementById('admin-modal-overlay').classList.contains('active') && typeof loadAdminData === 'function') {
                        loadAdminData();
                    }
                })
                .catch(function(err) {
                    alert('Failed to delete property: ' + err.message);
                });
            }
        };
    }
    var viewBtn = popupContent.querySelector('.view-pin-btn');
    if (viewBtn) {
        viewBtn.onclick = function(e) {
            e.stopPropagation();
            if (typeof openPropertyPanel === 'function') openPropertyPanel('view', index);
        };
    }

    return popupContent;
}

function togglePropertyVerification(propId, markerIndex, clickedBtn) {
    if (!currentUser || currentUser.role !== 'admin') return;
    var target = null;
    var targetIdx = -1;

    if (markerIndex !== undefined && markerIndex >= 0 && landlordMarkers[markerIndex]) {
        target = landlordMarkers[markerIndex];
        targetIdx = markerIndex;
    } else {
        for (var k = 0; k < landlordMarkers.length; k++) {
            if (landlordMarkers[k].id === propId) {
                target = landlordMarkers[k];
                targetIdx = k;
                break;
            }
        }
    }

    if (!target) return;

    var currentStatus = target.is_verified === 1 ? 1 : 0;
    var newStatus = currentStatus === 1 ? 0 : 1;

    if (clickedBtn) {
        clickedBtn.disabled = true;
        clickedBtn.innerText = 'Updating...';
    }

    fetch('/api/properties/' + propId + '/verify', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            admin_id: currentUser.id,
            admin_email: currentUser.email,
            is_verified: newStatus
        })
    })
    .then(function(res) { return res.json().then(function(d) { if (!res.ok) throw new Error(d.error || 'Failed to update status'); return d; }); })
    .then(function() {
        target.is_verified = newStatus;
        if (target.marker) {
            target.marker.setPopupContent(createMarkerPopup(targetIdx));
        }
        rebuildAllPopups();
        if (typeof applyFiltersToMap === 'function') applyFiltersToMap();
        if (document.getElementById('admin-modal-overlay').classList.contains('active') && typeof loadAdminData === 'function') {
            loadAdminData();
        }
    })
    .catch(function(err) {
        alert('Verification toggle failed: ' + err.message);
        if (clickedBtn) {
            clickedBtn.disabled = false;
            clickedBtn.innerText = currentStatus === 1 ? "✕ Hide from Map (Unapprove)" : "✓ Approve & Publish Pin";
        }
    });
}

function rebuildAllPopups() {
    for (var i = 0; i < landlordMarkers.length; i++) {
        var item = landlordMarkers[i];
        if (!item || !item.marker) continue;
        var newContent = createMarkerPopup(i);
        if (item.marker.getPopup()) {
            item.marker.setPopupContent(newContent);
        } else {
            item.marker.bindPopup(newContent);
        }
    }
}

// 7. Load properties from backend
function loadProperties() {
    var url = '/api/properties';
    if (currentUser && currentUser.id) {
        url += '?user_id=' + encodeURIComponent(currentUser.id);
    }
    fetch(url)
        .then(function(res) {
            if (res.headers && res.headers.get('X-User-Deleted') === 'true') {
                forceLogout('Your account has been deleted or is no longer active.');
            }
            return res.json();
        })
        .then(function(properties) {
            if (!Array.isArray(properties)) return;
            for (var i = 0; i < landlordMarkers.length; i++) {
                if (landlordMarkers[i] && landlordMarkers[i].marker) {
                    map.removeLayer(landlordMarkers[i].marker);
                }
            }
            landlordMarkers = [];

            for (var j = 0; j < properties.length; j++) {
                var prop = properties[j];

                var isOwner = currentUser && currentUser.id === prop.user_id;
                var isAdmin = currentUser && currentUser.role === 'admin';
                var isVerified = prop.is_verified === 1;

                if (!isVerified && !isAdmin && !isOwner) {
                    continue;
                }

                var marker = L.marker([prop.lat, prop.lng]).addTo(map);
                var propertyData = {
                    id: prop.id,
                    user_id: prop.user_id,
                    marker: marker,
                    name: prop.name,
                    desc: prop.desc,
                    price: prop.price,
                    phone: prop.phone,
                    landlord_name: prop.landlord_name,
                    is_verified: prop.is_verified || 0,
                    lat: prop.lat,
                    lng: prop.lng,
                    image: prop.image || '',
                    details: prop.details || ''
                };
                var index = landlordMarkers.length;
                landlordMarkers.push(propertyData);
                marker.bindPopup(createMarkerPopup(index));
                
                (function(m, idx) {
                    m.on('click', function(e) {
                        if (pendingMarker) {
                            map.removeLayer(pendingMarker);
                            pendingMarker = null;
                        }
                        if (typeof panelMode !== 'undefined' && panelMode === 'create' && typeof closePropertyPanel === 'function') {
                            closePropertyPanel();
                        }
                        map.panTo(e.latlng, { animate: true });
                        m.openPopup();
                    });
                    m.on('popupclose', function() {
                        var row = document.getElementById('popup-features-' + idx);
                        if (row) {
                            row.style.display = 'none';
                            var btn = row.previousElementSibling ? row.previousElementSibling.querySelector('.popup-reveal-btn') : null;
                            if (btn) {
                                btn.classList.remove('active');
                                btn.innerHTML = "<span class='reveal-dots-icon'>••••</span> <span class='reveal-btn-label'>Reveal Room Info</span>";
                            }
                        }
                    });
                })(marker, index);
            }

            if (typeof applyFiltersToMap === 'function') {
                applyFiltersToMap();
            }
        })
        .catch(function(err) {
            console.error('Failed to load properties:', err);
        });
}

// 8. Landlord map click listener (Drop pinpoint & open add panel)
map.on('click', function(e) {
    if (currentUser && currentUser.role === 'landlord') {
        if (!isInsideKuchingBoundary(e.latlng.lat, e.latlng.lng)) {
            alert("Please select a location within the Kuching area.");
            return;
        }
        var myCount = 0;
        for (var i = 0; i < landlordMarkers.length; i++) {
            if (landlordMarkers[i].user_id === currentUser.id) {
                myCount++;
            }
        }
        if (myCount >= 2) {
            alert("You can only add up to 2 property pinpoints.");
            return;
        }
        pendingLatLng = e.latlng;
        if (pendingMarker) {
            map.removeLayer(pendingMarker);
        }
        pendingMarker = L.marker(pendingLatLng, { opacity: 0.8 }).addTo(map);
        if (typeof openPropertyPanel === 'function') {
            openPropertyPanel('create');
        }
    }
});

// Initial load
loadProperties();
