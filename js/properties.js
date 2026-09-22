/**
 * PoliSewa - Property Management & Showcase Panel Module (js/properties.js)
 * Controls property creation, editing, viewing, photo uploads, specifications & bottom-sheet gestures.
 */

var panelMode = 'create'; // 'create' | 'edit' | 'view'
var editingMarkerIndex = -1;
var pendingImages = []; // Array of { url: string, file: File | null }

// 1. Accordion & Specifications Form Helpers
function toggleAccordion(id) {
    var el = document.getElementById(id);
    if (el) {
        el.classList.toggle('collapsed');
    }
}

function parsePropertyDetails(details) {
    if (!details) return null;
    if (typeof details === 'object') return details;
    if (typeof details === 'string') {
        var trimmed = details.trim();
        if (!trimmed || trimmed === '""' || trimmed === '{}') return null;
        try {
            return JSON.parse(trimmed);
        } catch (e) {
            return null;
        }
    }
    return null;
}

function collectPropertyDetailsFromPanel() {
    var getCheckedValues = function (name) {
        var checked = [];
        var inputs = document.querySelectorAll('input[name="' + name + '"]:checked');
        for (var i = 0; i < inputs.length; i++) {
            checked.push(inputs[i].value);
        }
        return checked;
    };

    var getRadioValue = function (name) {
        var checked = document.querySelector('input[name="' + name + '"]:checked');
        return checked ? checked.value : '';
    };

    return {
        floor_level: getCheckedValues('prop_floor_level'),
        room_type: getRadioValue('prop_room_type'),
        bathroom_type: getRadioValue('prop_bathroom_type'),
        utilities: getCheckedValues('prop_utilities'),
        preferences: {
            general: getCheckedValues('prop_pref_general'),
            race: getCheckedValues('prop_pref_race'),
            occupation: getCheckedValues('prop_pref_occupation')
        }
    };
}

function resetPropertyDetailsForm() {
    var names = ['prop_floor_level', 'prop_room_type', 'prop_bathroom_type', 'prop_utilities', 'prop_pref_general', 'prop_pref_race', 'prop_pref_occupation'];
    for (var i = 0; i < names.length; i++) {
        var inputs = document.querySelectorAll('input[name="' + names[i] + '"]');
        for (var j = 0; j < inputs.length; j++) {
            inputs[j].checked = false;
        }
    }
}

function populatePropertyDetailsForm(details) {
    resetPropertyDetailsForm();
    var data = parsePropertyDetails(details);
    if (!data || typeof data !== 'object') return;

    var setChecked = function (name, values) {
        if (!values || !Array.isArray(values)) return;
        var inputs = document.querySelectorAll('input[name="' + name + '"]');
        for (var i = 0; i < inputs.length; i++) {
            inputs[i].checked = (values.indexOf(inputs[i].value) !== -1);
        }
    };

    var setRadio = function (name, val) {
        if (!val) return;
        var inputs = document.querySelectorAll('input[name="' + name + '"]');
        for (var i = 0; i < inputs.length; i++) {
            inputs[i].checked = (inputs[i].value === val);
        }
    };

    setChecked('prop_floor_level', data.floor_level);
    setRadio('prop_room_type', data.room_type);
    setRadio('prop_bathroom_type', data.bathroom_type);
    setChecked('prop_utilities', data.utilities);

    if (data.preferences) {
        setChecked('prop_pref_general', data.preferences.general);
        setChecked('prop_pref_race', data.preferences.race);
        setChecked('prop_pref_occupation', data.preferences.occupation);
    }
}

// 2. Render Property Details Showcase View (Student/Viewer mode)
function renderPropertyDetailsView(details) {
    var container = document.getElementById('panel-room-details-view');
    if (!container) return;
    container.innerHTML = '';

    var data = parsePropertyDetails(details);
    if (!data || typeof data !== 'object') {
        container.innerHTML = '<div class="detail-view-card" style="background:#f8fafc; border:1px dashed #cbd5e1; text-align:center; padding:16px 14px;">' +
            '<div style="font-size:22px; margin-bottom:4px;">🛏️</div>' +
            '<div style="font-weight:700; color:#334155; font-size:13.5px;">Standard Room Rental</div>' +
            '<div style="font-size:12px; color:#64748b; margin-top:2px;">Contact landlord directly via phone or WhatsApp for specific room amenities & details.</div>' +
            '</div>';
        return;
    }

    var html = '';

    // Room Specifications
    var hasRoomSpecs = (data.floor_level && data.floor_level.length > 0) || data.room_type || data.bathroom_type;
    if (hasRoomSpecs) {
        html += '<div class="detail-view-card">' +
            '<div class="detail-view-card-title">🏢 Room Specifications</div>' +
            '<div class="detail-badges-grid">';
        if (data.room_type) {
            html += '<span class="detail-badge-pill pill-primary">🛏️ ' + escapeHtml(data.room_type) + ' Room</span>';
        }
        if (data.bathroom_type) {
            html += '<span class="detail-badge-pill pill-primary">🚿 ' + escapeHtml(data.bathroom_type) + ' Bathroom</span>';
        }
        if (data.floor_level && data.floor_level.length > 0) {
            var fls = Array.isArray(data.floor_level) ? data.floor_level : [data.floor_level];
            for (var f = 0; f < fls.length; f++) {
                html += '<span class="detail-badge-pill">🏢 ' + escapeHtml(fls[f]) + ' Floor</span>';
            }
        }
        html += '</div></div>';
    }

    // Utilities & Amenities
    if (data.utilities && data.utilities.length > 0) {
        var utilIcons = {
            'Air-Conditioning': '❄️',
            'Washing Machine': '🧺',
            'Wifi / Internet Access': '📶',
            'Cooking Allowed': '🍳',
            'TV': '📺',
            'Share Bathroom': '🚻',
            'Private Bathroom': '🚿',
            'Shower': '🚿'
        };
        html += '<div class="detail-view-card">' +
            '<div class="detail-view-card-title">⚡ Utilities & Amenities</div>' +
            '<div class="detail-badges-grid">';
        var utilsList = Array.isArray(data.utilities) ? data.utilities : [data.utilities];
        for (var i = 0; i < utilsList.length; i++) {
            var uName = utilsList[i];
            var icon = utilIcons[uName] || '✓';
            html += '<span class="detail-badge-pill pill-success">' + icon + ' ' + escapeHtml(uName) + '</span>';
        }
        html += '</div></div>';
    }

    // Rental Preferences
    var hasGeneralPref = data.preferences && data.preferences.general && data.preferences.general.length > 0;
    if (hasGeneralPref) {
        var prefIcons = {
            'Preferred Listing': '⭐',
            'Prefer Zero Deposit': '💰',
            'Prefer move-in immediately': '🚀',
            'Prefer pet allowed': '🐾',
            'Prefer muslim friendly': '🕌',
            'Prefer smoking allowed': '🚬'
        };
        html += '<div class="detail-view-card">' +
            '<div class="detail-view-card-title">📋 Rental Preferences</div>' +
            '<div class="detail-badges-grid">';
        var genList = Array.isArray(data.preferences.general) ? data.preferences.general : [data.preferences.general];
        for (var j = 0; j < genList.length; j++) {
            var pName = genList[j];
            var pIcon = prefIcons[pName] || '✓';
            html += '<span class="detail-badge-pill pill-purple">' + pIcon + ' ' + escapeHtml(pName) + '</span>';
        }
        html += '</div></div>';
    }

    // Preferred Tenant Criteria
    var hasRace = data.preferences && data.preferences.race && data.preferences.race.length > 0;
    var hasOcc = data.preferences && data.preferences.occupation && data.preferences.occupation.length > 0;
    if (hasRace || hasOcc) {
        html += '<div class="detail-view-card">' +
            '<div class="detail-view-card-title">👥 Preferred Tenant Criteria</div>' +
            '<div class="detail-badges-grid">';
        if (hasRace) {
            var raceList = Array.isArray(data.preferences.race) ? data.preferences.race : [data.preferences.race];
            for (var r = 0; r < raceList.length; r++) {
                html += '<span class="detail-badge-pill">👤 Race: ' + escapeHtml(raceList[r]) + '</span>';
            }
        }
        if (hasOcc) {
            var occList = Array.isArray(data.preferences.occupation) ? data.preferences.occupation : [data.preferences.occupation];
            for (var o = 0; o < occList.length; o++) {
                html += '<span class="detail-badge-pill">💼 Occupation: ' + escapeHtml(occList[o]) + '</span>';
            }
        }
        html += '</div></div>';
    }

    container.innerHTML = html;
}

// 3. Panel Photo Gallery & Multi-Upload Handlers
function renderPanelImages(mode) {
    var editContainer = document.getElementById('panel-image-edit-container');
    var viewContainer = document.getElementById('panel-image-view-container');
    var grid = document.getElementById('panel-image-grid');
    var galleryView = document.getElementById('panel-gallery-view');
    var label = document.getElementById('panel-image-label');

    if (mode === 'create' || mode === 'edit') {
        if (label) label.innerHTML = 'Property Photos (' + pendingImages.length + ' / 10) <span class="required-star">*</span>';
        if (editContainer) editContainer.style.display = 'block';
        if (viewContainer) viewContainer.style.display = 'none';

        var gridHtml = '';
        for (var i = 0; i < pendingImages.length; i++) {
            var item = pendingImages[i];
            gridHtml += '<div class="panel-image-card ' + (i === 0 ? 'is-cover' : '') + '">' +
                '<img src="' + item.url + '" alt="Property photo ' + (i + 1) + '" />' +
                (i === 0 ? '<span class="cover-badge">Cover</span>' : '') +
                '<button type="button" class="remove-btn" onclick="removePendingImage(' + i + ')" title="Remove photo" aria-label="Remove photo">✕</button>' +
                '</div>';
        }
        if (pendingImages.length < 10) {
            gridHtml += '<div class="panel-add-card" onclick="document.getElementById(\'panel-image-input\').click()">' +
                '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>' +
                '<span>Add Photo</span>' +
                '</div>';
        }
        if (grid) grid.innerHTML = gridHtml;
    } else {
        if (label) label.innerText = 'Property Photos';
        if (editContainer) editContainer.style.display = 'none';
        if (viewContainer) viewContainer.style.display = 'block';
        var urls = pendingImages.map(function (item) { return item.url; });
        if (galleryView) galleryView.innerHTML = buildGalleryHtml(urls, 'panel-view-gallery', false);
    }
}

function handleImageSelection(event) {
    var files = event.target.files;
    if (!files || files.length === 0) return;
    var maxAllowed = 10 - pendingImages.length;
    if (maxAllowed <= 0) {
        alert('Maximum 10 photos allowed per property.');
        event.target.value = '';
        return;
    }

    var countToAdd = Math.min(files.length, maxAllowed);
    for (var i = 0; i < countToAdd; i++) {
        var file = files[i];
        var tempUrl = URL.createObjectURL(file);
        pendingImages.push({ url: tempUrl, file: file });
    }
    event.target.value = '';
    renderPanelImages(panelMode);
}

function removePendingImage(index) {
    pendingImages.splice(index, 1);
    renderPanelImages(panelMode);
}

// 4. Open / Close Property Panel
function openPropertyPanel(mode, index) {
    panelMode = mode;
    if (mode !== 'create' && pendingMarker) {
        map.removeLayer(pendingMarker);
        pendingMarker = null;
        pendingLatLng = null;
    }
    var panel = document.getElementById('property-panel');
    var title = document.getElementById('panel-title-text');
    var saveBtn = document.getElementById('panel-save-btn');
    var deleteBtn = document.getElementById('panel-delete-btn');
    var nameInput = document.getElementById('panel-name');
    var descInput = document.getElementById('panel-desc');
    var priceInput = document.getElementById('panel-price');
    var phoneInput = document.getElementById('panel-phone');
    var actionsEdit = document.getElementById('panel-actions-edit');
    var actionsView = document.getElementById('panel-actions-view');
    var landlordInfo = document.getElementById('panel-landlord-info');
    var panelViewSection = document.getElementById('panel-view-section');
    var panelEditSection = document.getElementById('panel-edit-section');
    var showcaseTitle = document.getElementById('showcase-title');
    var showcaseBadge = document.getElementById('showcase-badge');
    var showcasePrice = document.getElementById('showcase-price');
    var showcaseDesc = document.getElementById('showcase-desc');

    if (mode === 'create') {
        title.innerText = 'Add Property Listing';
        saveBtn.innerText = 'Add Property';
        if (deleteBtn) deleteBtn.style.display = 'none';
        if (panelViewSection) panelViewSection.style.display = 'none';
        if (panelEditSection) {
            panelEditSection.style.display = 'flex';
            panelEditSection.style.flexDirection = 'column';
        }
        nameInput.value = '';
        descInput.value = '';
        priceInput.value = '';
        phoneInput.value = (currentUser && currentUser.phone) ? currentUser.phone : '';
        landlordInfo.innerHTML = '';
        resetPropertyDetailsForm();
        actionsEdit.style.display = 'flex';
        actionsView.style.display = 'none';
        pendingImages = [];
        renderPanelImages('create');
    } else if (mode === 'edit') {
        editingMarkerIndex = index;
        var data = landlordMarkers[index];
        title.innerText = 'Edit Property';
        saveBtn.innerText = 'Save Changes';
        if (deleteBtn) deleteBtn.style.display = 'inline-block';
        if (panelViewSection) panelViewSection.style.display = 'none';
        if (panelEditSection) {
            panelEditSection.style.display = 'flex';
            panelEditSection.style.flexDirection = 'column';
        }
        nameInput.value = data.name || '';
        descInput.value = data.desc || '';
        priceInput.value = data.price || '';
        phoneInput.value = data.phone || '';
        landlordInfo.innerHTML = '';
        populatePropertyDetailsForm(data.details);
        actionsEdit.style.display = 'flex';
        actionsView.style.display = 'none';
        var urls = parseImageUrls(data.image);
        pendingImages = urls.map(function (u) { return { url: u, file: null }; });
        renderPanelImages('edit');
    } else if (mode === 'view') {
        var viewData = landlordMarkers[index];
        title.innerText = 'Property Showcase';
        if (panelEditSection) panelEditSection.style.display = 'none';
        if (panelViewSection) {
            panelViewSection.style.display = 'flex';
            panelViewSection.style.flexDirection = 'column';
        }
        actionsEdit.style.display = 'none';
        actionsView.style.display = 'flex';

        if (showcaseTitle) showcaseTitle.innerText = viewData.name || 'Room Rental';
        if (showcaseBadge) {
            showcaseBadge.innerHTML = viewData.is_verified === 1
                ? '<span style="background:#ecfdf5;color:#059669;padding:4px 10px;border-radius:20px;font-size:12px;font-weight:700;border:1px solid #a7f3d0;">✓ Verified</span>'
                : '<span style="background:#fef3c7;color:#d97706;padding:4px 10px;border-radius:20px;font-size:12px;font-weight:700;border:1px solid #fde68a;">⏳ Pending</span>';
        }
        if (showcasePrice) showcasePrice.innerText = 'RM ' + (viewData.price || '0');
        if (showcaseDesc) showcaseDesc.innerText = viewData.desc || 'No description provided.';

        renderPropertyDetailsView(viewData.details);

        var viewUrls = parseImageUrls(viewData.image);
        pendingImages = viewUrls.map(function (u) { return { url: u, file: null }; });
        renderPanelImages('view');

        var lHtml = '<div style="margin-top:16px;padding:14px 16px;background:#f8fafc;border-radius:12px;border:1px solid #e2e8f0;">' +
            '<div style="font-size:11.5px;font-weight:700;text-transform:uppercase;color:#64748b;letter-spacing:0.5px;margin-bottom:6px;">Landlord Contact</div>' +
            '<div style="font-weight:700;font-size:15px;color:#1e293b;margin-bottom:4px;">' + escapeHtml(viewData.landlord_name || 'Landlord') + '</div>' +
            '<div style="font-size:13px;color:#475569;margin-bottom:10px;">📞 ' + escapeHtml(viewData.phone || 'N/A') + '</div>' +
            buildContactButtonsHtml(viewData.phone) +
            '</div>';
        landlordInfo.innerHTML = lHtml;
    }

    panel.classList.add('active');
}

function closePropertyPanel() {
    var panel = document.getElementById('property-panel');
    if (panel) panel.classList.remove('active');
    editingMarkerIndex = -1;
    pendingImages = [];
    resetPropertyDetailsForm();
    var roomViewContainer = document.getElementById('panel-room-details-view');
    if (roomViewContainer) roomViewContainer.innerHTML = '';
    if (pendingMarker) {
        map.removeLayer(pendingMarker);
        pendingMarker = null;
    }
    var input = document.getElementById('panel-image-input');
    if (input) input.value = '';
}

// 5. Save & Delete Property Handlers
function savePropertyFromPanel(event) {
    event.preventDefault();

    var name = document.getElementById('panel-name').value.trim();
    var desc = document.getElementById('panel-desc').value.trim();
    var price = document.getElementById('panel-price').value.trim();
    var phone = document.getElementById('panel-phone').value.trim();

    if (!name) {
        alert('Property / Room Name is mandatory and cannot be empty.');
        document.getElementById('panel-name').focus();
        return;
    }
    if (!desc) {
        alert('Description is mandatory and cannot be empty.');
        document.getElementById('panel-desc').focus();
        return;
    }
    if (!price || isNaN(price) || parseFloat(price) <= 0) {
        alert('Monthly Rent (RM) is mandatory and must be a valid amount greater than 0.');
        document.getElementById('panel-price').focus();
        return;
    }
    if (!phone) {
        alert('Contact Phone Number is mandatory and cannot be empty.');
        document.getElementById('panel-phone').focus();
        return;
    }
    if (!pendingImages || pendingImages.length === 0) {
        alert('Property Photos are mandatory. Please upload at least 1 photo.');
        document.getElementById('panel-image-input').click();
        return;
    }

    var saveBtn = document.getElementById('panel-save-btn');
    var originalText = saveBtn.innerText;
    saveBtn.disabled = true;
    saveBtn.innerText = 'Saving...';

    var newFiles = pendingImages.filter(function (item) { return item.file !== null; });

    var savePropertyWithFinalUrls = function (finalImageUrls) {
        var finalImageStr = JSON.stringify(finalImageUrls);
        var detailsObj = collectPropertyDetailsFromPanel();
        var detailsStr = JSON.stringify(detailsObj);

        if (panelMode === 'create') {
            fetch('/api/properties', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: currentUser.id,
                    name: name,
                    desc: desc,
                    price: price,
                    phone: phone,
                    lat: pendingLatLng.lat,
                    lng: pendingLatLng.lng,
                    image: finalImageStr,
                    details: detailsStr
                })
            })
                .then(function (res) {
                    return res.json().then(function (d) {
                        if (!res.ok) {
                            if (res.status === 401 && d.error && d.error.includes('deleted')) {
                                forceLogout(d.error);
                            }
                            throw new Error(d.error || 'Failed to create property.');
                        }
                        return d;
                    });
                })
                .then(function (result) {
                    if (pendingMarker) {
                        map.removeLayer(pendingMarker);
                        pendingMarker = null;
                    }
                    var marker = L.marker([pendingLatLng.lat, pendingLatLng.lng]).addTo(map);
                    var propertyData = {
                        id: result.id,
                        user_id: currentUser.id,
                        marker: marker,
                        name: name,
                        desc: desc,
                        price: price,
                        phone: phone,
                        landlord_name: currentUser.name || '',
                        is_verified: 0,
                        lat: pendingLatLng.lat,
                        lng: pendingLatLng.lng,
                        image: finalImageStr,
                        details: detailsStr
                    };
                    var newIndex = landlordMarkers.length;
                    landlordMarkers.push(propertyData);
                    marker.bindPopup(createMarkerPopup(newIndex));

                    (function (m, idx) {
                        m.on('click', function (e) {
                            if (pendingMarker) {
                                map.removeLayer(pendingMarker);
                                pendingMarker = null;
                            }
                            if (panelMode === 'create') closePropertyPanel();
                            map.panTo(e.latlng, { animate: true });
                            m.openPopup();
                        });
                    })(marker, newIndex);

                    closePropertyPanel();
                    rebuildAllPopups();
                    if (typeof applyFiltersToMap === 'function') applyFiltersToMap();
                    alert('Property added successfully! It is now pending admin approval.');
                })
                .catch(function (err) {
                    alert(err.message);
                })
                .finally(function () {
                    saveBtn.disabled = false;
                    saveBtn.innerText = originalText;
                });

        } else if (panelMode === 'edit') {
            var targetIndex = editingMarkerIndex;
            if (targetIndex < 0 || !landlordMarkers[targetIndex]) {
                alert('Property to edit could not be found.');
                saveBtn.disabled = false;
                saveBtn.innerText = originalText;
                return;
            }

            var prop = landlordMarkers[targetIndex];
            fetch('/api/properties/' + prop.id + '?user_id=' + currentUser.id, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: currentUser.id,
                    name: name,
                    desc: desc,
                    price: price,
                    phone: phone,
                    image: finalImageStr,
                    details: detailsStr
                })
            })
                .then(function (res) {
                    return res.json().then(function (d) {
                        if (!res.ok) throw new Error(d.error || 'Failed to update property.');
                        return d;
                    });
                })
                .then(function () {
                    prop.name = name;
                    prop.desc = desc;
                    prop.price = price;
                    prop.phone = phone;
                    prop.image = finalImageStr;
                    prop.details = detailsStr;

                    prop.marker.setPopupContent(createMarkerPopup(targetIndex));
                    closePropertyPanel();
                    rebuildAllPopups();
                    if (typeof applyFiltersToMap === 'function') applyFiltersToMap();
                    alert('Property updated successfully!');
                })
                .catch(function (err) {
                    alert(err.message);
                })
                .finally(function () {
                    saveBtn.disabled = false;
                    saveBtn.innerText = originalText;
                });
        }
    };

    if (newFiles.length > 0) {
        var formData = new FormData();
        newFiles.forEach(function (item) {
            formData.append('images', item.file);
        });
        fetch('/api/properties/upload-images', {
            method: 'POST',
            body: formData
        })
            .then(function (res) {
                return res.json().then(function (d) {
                    if (!res.ok) throw new Error(d.error || 'Failed to upload images.');
                    return d;
                });
            })
            .then(function (uploadResult) {
                var uploadedUrls = uploadResult.imageUrls || [];
                var uploadedIdx = 0;
                var finalUrls = pendingImages.map(function (item) {
                    if (item.file !== null && uploadedUrls[uploadedIdx]) {
                        return uploadedUrls[uploadedIdx++];
                    }
                    return item.url;
                });
                savePropertyWithFinalUrls(finalUrls);
            })
            .catch(function (err) {
                alert('Image upload failed: ' + err.message);
                saveBtn.disabled = false;
                saveBtn.innerText = originalText;
            });
    } else {
        var finalUrls = pendingImages.map(function (item) { return item.url; });
        savePropertyWithFinalUrls(finalUrls);
    }
}

function deletePropertyFromPanel() {
    if (editingMarkerIndex < 0 || !landlordMarkers[editingMarkerIndex]) return;
    var targetIndex = editingMarkerIndex;
    var data = landlordMarkers[targetIndex];

    if (confirm('Delete this property listing?')) {
        fetch('/api/properties/' + data.id + '?user_id=' + currentUser.id, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: currentUser.id })
        })
            .then(function (res) { return res.json(); })
            .then(function (result) {
                if (result.error) {
                    alert(result.error);
                    return;
                }
                map.removeLayer(data.marker);
                landlordMarkers.splice(targetIndex, 1);
                closePropertyPanel();
                rebuildAllPopups();
                if (typeof applyFiltersToMap === 'function') applyFiltersToMap();
            })
            .catch(function (err) {
                alert('Failed to delete property: ' + err.message);
            });
    }
}
