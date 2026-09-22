/**
 * PoliSewa - Unified Search & Property Filter Module (js/filter.js)
 * Manages search autocompletion (OSM + DB listings), filter criteria modal, and live map filtering.
 */

var activeFilters = {
    maxPrice: null,
    roomTypes: [],
    bathroomType: '',
    utilities: [],
    floorLevels: [],
    generalPrefs: [],
    occupationPrefs: []
};

var searchDebounceTimer = null;

// 1. Filter Modal & Quick Price Controls
function openFilterModal() {
    var searchBox = document.getElementById('search-box');
    var resultsContainer = document.getElementById('search-results');
    if (resultsContainer) resultsContainer.style.display = 'none';
    if (searchBox) searchBox.classList.remove('has-results');

    syncFilterFormWithActive();
    onFilterCriteriaChanged();

    var filterModalOverlay = document.getElementById('filter-modal-overlay');
    if (filterModalOverlay) {
        filterModalOverlay.classList.add('active');
    }
}

function closeFilterModal() {
    var filterModalOverlay = document.getElementById('filter-modal-overlay');
    if (filterModalOverlay) {
        filterModalOverlay.classList.remove('active');
    }
}

function setQuickPrice(val) {
    var input = document.getElementById('filter-max-price');
    if (input) {
        input.value = val ? val : '';
        updateQuickChipActive(val);
        onFilterCriteriaChanged();
    }
}

function updateQuickChipActive(currentVal) {
    var chips = document.querySelectorAll('.quick-chip, .quick-price-chip');
    var parsedCurrent = (currentVal !== null && currentVal !== '' && !isNaN(currentVal)) ? parseFloat(currentVal) : null;
    for (var i = 0; i < chips.length; i++) {
        var chip = chips[i];
        var onclickAttr = chip.getAttribute('onclick') || '';
        var match = onclickAttr.match(/setQuickPrice\((\d+|'')?\)/);
        var chipVal = (match && match[1] && match[1] !== "''") ? parseFloat(match[1]) : null;
        if ((parsedCurrent === null && chipVal === null) || (parsedCurrent !== null && chipVal === parsedCurrent)) {
            chip.classList.add('active');
        } else {
            chip.classList.remove('active');
        }
    }
}

function getFormFilterValues() {
    var priceInput = document.getElementById('filter-max-price');
    var rawPrice = priceInput ? priceInput.value.trim() : '';
    var maxPrice = (rawPrice !== '' && !isNaN(rawPrice)) ? parseFloat(rawPrice) : null;

    var getChecked = function (name) {
        var checked = [];
        var inputs = document.querySelectorAll('input[name="' + name + '"]:checked');
        for (var i = 0; i < inputs.length; i++) {
            checked.push(inputs[i].value);
        }
        return checked;
    };

    var bathRadio = document.querySelector('input[name="filter_bathroom_type"]:checked');
    var bathroomType = bathRadio ? bathRadio.value : '';

    return {
        maxPrice: maxPrice,
        roomTypes: getChecked('filter_room_type'),
        bathroomType: bathroomType,
        utilities: getChecked('filter_utilities'),
        floorLevels: getChecked('filter_floor_level'),
        generalPrefs: getChecked('filter_pref_general'),
        occupationPrefs: getChecked('filter_pref_occupation')
    };
}

function syncFilterFormWithActive() {
    var priceInput = document.getElementById('filter-max-price');
    if (priceInput) {
        priceInput.value = (activeFilters.maxPrice !== null && activeFilters.maxPrice > 0) ? activeFilters.maxPrice : '';
        updateQuickChipActive(activeFilters.maxPrice);
    }

    var setChecked = function (name, list) {
        var inputs = document.querySelectorAll('input[name="' + name + '"]');
        for (var i = 0; i < inputs.length; i++) {
            inputs[i].checked = (list && list.indexOf(inputs[i].value) !== -1);
        }
    };

    setChecked('filter_room_type', activeFilters.roomTypes);
    setChecked('filter_utilities', activeFilters.utilities);
    setChecked('filter_floor_level', activeFilters.floorLevels);
    setChecked('filter_pref_general', activeFilters.generalPrefs);
    setChecked('filter_pref_occupation', activeFilters.occupationPrefs);

    var bathRadios = document.querySelectorAll('input[name="filter_bathroom_type"]');
    for (var b = 0; b < bathRadios.length; b++) {
        bathRadios[b].checked = (bathRadios[b].value === activeFilters.bathroomType);
    }
}

// 2. Filter Evaluation & Criteria Checking
function hasActiveFilter(filters) {
    if (!filters) return false;
    if (filters.maxPrice !== null && filters.maxPrice > 0) return true;
    if (filters.roomTypes && filters.roomTypes.length > 0) return true;
    if (filters.bathroomType && filters.bathroomType !== '') return true;
    if (filters.utilities && filters.utilities.length > 0) return true;
    if (filters.floorLevels && filters.floorLevels.length > 0) return true;
    if (filters.generalPrefs && filters.generalPrefs.length > 0) return true;
    if (filters.occupationPrefs && filters.occupationPrefs.length > 0) return true;
    return false;
}

function countActiveFilterCriteria(filters) {
    if (!filters) return 0;
    var count = 0;
    if (filters.maxPrice !== null && filters.maxPrice > 0) count++;
    if (filters.roomTypes && filters.roomTypes.length > 0) count += filters.roomTypes.length;
    if (filters.bathroomType && filters.bathroomType !== '') count++;
    if (filters.utilities && filters.utilities.length > 0) count += filters.utilities.length;
    if (filters.floorLevels && filters.floorLevels.length > 0) count += filters.floorLevels.length;
    if (filters.generalPrefs && filters.generalPrefs.length > 0) count += filters.generalPrefs.length;
    if (filters.occupationPrefs && filters.occupationPrefs.length > 0) count += filters.occupationPrefs.length;
    return count;
}

function propertyMatchesFilters(prop, filters) {
    if (!filters || !hasActiveFilter(filters)) return true;

    // Price Budget Check
    if (filters.maxPrice !== null && filters.maxPrice > 0) {
        var pVal = parseFloat(prop.price);
        if (isNaN(pVal) || pVal > filters.maxPrice) {
            return false;
        }
    }

    var d = (typeof parsePropertyDetails === 'function') ? parsePropertyDetails(prop.details) : null;
    var detailsStr = '';
    if (prop.details) {
        if (typeof prop.details === 'string') {
            detailsStr = prop.details;
        } else {
            try { detailsStr = JSON.stringify(prop.details); } catch (e) { }
        }
    }
    // Search corpus combining property name, description, and raw details text
    var fullCorpus = ((prop.name || '') + ' ' + (prop.desc || '') + ' ' + detailsStr).toLowerCase();

    // Helper to test if any keyword in an array appears in fullCorpus
    var matchesAny = function (keywords) {
        for (var k = 0; k < keywords.length; k++) {
            if (fullCorpus.includes(keywords[k].toLowerCase())) return true;
        }
        return false;
    };

    // Room Type Check
    if (filters.roomTypes && filters.roomTypes.length > 0) {
        var matchedRoom = false;
        if (d && d.room_type && filters.roomTypes.indexOf(d.room_type) !== -1) {
            matchedRoom = true;
        }
        if (!matchedRoom) {
            for (var r = 0; r < filters.roomTypes.length; r++) {
                var rt = filters.roomTypes[r];
                var rtSynonyms = [rt.toLowerCase()];
                if (rt === 'Single') rtSynonyms.push('bujang', 'non-sharing', 'single room', '1 orang', 'seorang');
                else if (rt === 'Master') rtSynonyms.push('master room', 'bilik master', 'utama', 'bilik besar');
                else if (rt === 'Middle') rtSynonyms.push('middle room', 'bilik middle', 'tengah', 'medium');
                else if (rt === 'Studio') rtSynonyms.push('studio unit', 'bilik studio');
                else if (rt === 'Guest') rtSynonyms.push('guest room', 'tetamu');
                else if (rt === 'Suite') rtSynonyms.push('suite');

                if (matchesAny(rtSynonyms)) {
                    matchedRoom = true;
                    break;
                }
            }
        }
        if (!matchedRoom) return false;
    }

    // Bathroom Type Check
    if (filters.bathroomType) {
        var matchedBath = false;
        if (d && d.bathroom_type && d.bathroom_type.toLowerCase() === filters.bathroomType.toLowerCase()) {
            matchedBath = true;
        }
        if (!matchedBath) {
            if (filters.bathroomType.toLowerCase() === 'private') {
                matchedBath = matchesAny(['private', 'peribadi', 'bilik air peribadi', 'bilik air sendiri', 'attached bathroom', 'tandas sendiri', 'bilik air dalam bilik']);
            } else if (filters.bathroomType.toLowerCase() === 'shared') {
                matchedBath = matchesAny(['shared', 'share bathroom', 'shared bathroom', 'bilik air berkongsi', 'bilik air kongsi', 'kongsi bilik air', 'tandas kongsi', 'tandas berkongsi', 'luar bilik']);
            } else {
                matchedBath = fullCorpus.includes(filters.bathroomType.toLowerCase());
            }
        }
        if (!matchedBath) return false;
    }

    // Utilities Check
    if (filters.utilities && filters.utilities.length > 0) {
        var propUtils = (d && Array.isArray(d.utilities)) ? d.utilities : [];
        for (var u = 0; u < filters.utilities.length; u++) {
            var reqUtil = filters.utilities[u];
            var hasUtil = propUtils.indexOf(reqUtil) !== -1;
            if (!hasUtil) {
                var uSynonyms = [reqUtil.toLowerCase()];
                if (reqUtil.includes('Wifi')) {
                    uSynonyms.push('wifi', 'wi-fi', 'internet', 'unifi');
                } else if (reqUtil === 'Air-Conditioning') {
                    uSynonyms.push('aircond', 'air-con', 'air con', 'air conditioner', 'hawa dingin', 'berhawa dingin');
                } else if (reqUtil === 'Washing Machine') {
                    uSynonyms.push('mesin basuh', 'washing machine', 'dobi');
                } else if (reqUtil === 'Cooking Allowed') {
                    uSynonyms.push('cooking', 'dapur', 'masak', 'dapur masak');
                } else if (reqUtil === 'TV') {
                    uSynonyms.push('tv', 'televisyen');
                } else if (reqUtil === 'Shower') {
                    uSynonyms.push('shower', 'water heater', 'pemanas air', 'mandi');
                }
                hasUtil = matchesAny(uSynonyms);
            }
            if (!hasUtil) return false;
        }
    }

    // Floor Level Check
    if (filters.floorLevels && filters.floorLevels.length > 0) {
        var propFloors = (d && Array.isArray(d.floor_level)) ? d.floor_level : (d && d.floor_level ? [d.floor_level] : []);
        var matchedFloor = false;
        for (var f = 0; f < filters.floorLevels.length; f++) {
            var fl = filters.floorLevels[f];
            if (propFloors.indexOf(fl) !== -1) {
                matchedFloor = true;
                break;
            }
            var flSynonyms = [fl.toLowerCase() + ' floor'];
            if (fl === 'Ground') flSynonyms.push('ground', 'tingkat bawah', 'tingkat dasar');
            else if (fl === 'Low') flSynonyms.push('low floor', 'tingkat rendah', 'tingkat 1', 'tingkat 2');
            else if (fl === 'Mid') flSynonyms.push('mid floor', 'tingkat pertengahan', 'tingkat 3', 'tingkat 4');
            else if (fl === 'High') flSynonyms.push('high floor', 'tingkat tinggi', 'tingkat atas');
            else if (fl === 'Penthouse') flSynonyms.push('penthouse');

            if (matchesAny(flSynonyms)) {
                matchedFloor = true;
                break;
            }
        }
        if (!matchedFloor) return false;
    }

    // General Preferences Check
    if (filters.generalPrefs && filters.generalPrefs.length > 0) {
        var propGen = (d && d.preferences && Array.isArray(d.preferences.general)) ? d.preferences.general : [];
        for (var g = 0; g < filters.generalPrefs.length; g++) {
            var reqPref = filters.generalPrefs[g];
            var hasPref = propGen.indexOf(reqPref) !== -1;
            if (!hasPref) {
                var gSynonyms = [reqPref.replace('Prefer ', '').toLowerCase()];
                if (reqPref.includes('muslim')) {
                    gSynonyms.push('muslim', 'islam', 'lelaki muslim', 'perempuan muslim');
                } else if (reqPref.includes('Zero Deposit')) {
                    gSynonyms.push('zero deposit', 'tanpa deposit', 'tiada deposit', '0 deposit');
                } else if (reqPref.includes('move-in immediately')) {
                    gSynonyms.push('kemasukan segera', 'segera', 'move-in immediately', 'ready to move', 'urgent');
                } else if (reqPref.includes('pet allowed')) {
                    gSynonyms.push('pet allowed', 'haiwan', 'peliharaan', 'pets');
                } else if (reqPref.includes('smoking allowed')) {
                    gSynonyms.push('smoking allowed', 'merokok');
                }
                hasPref = matchesAny(gSynonyms);
            }
            if (!hasPref) return false;
        }
    }

    // Occupation Preference Check
    if (filters.occupationPrefs && filters.occupationPrefs.length > 0) {
        var propOcc = (d && d.preferences && Array.isArray(d.preferences.occupation)) ? d.preferences.occupation : [];
        for (var o = 0; o < filters.occupationPrefs.length; o++) {
            var reqOcc = filters.occupationPrefs[o];
            var hasOcc = propOcc.indexOf(reqOcc) !== -1;
            if (!hasOcc) {
                var oSynonyms = [reqOcc.toLowerCase()];
                if (reqOcc.toLowerCase() === 'student') {
                    oSynonyms.push('pelajar', 'student', 'pks', 'politeknik', 'mahasiswa');
                }
                hasOcc = matchesAny(oSynonyms);
            }
            if (!hasOcc) return false;
        }
    }

    return true;
}

// 3. Dynamic Filter Form Handlers & Map Sync
function onFilterCriteriaChanged() {
    var tempFilters = getFormFilterValues();
    updateQuickChipActive(tempFilters.maxPrice);
    var priceDisplay = document.getElementById('filter-price-display');
    if (priceDisplay) {
        if (tempFilters.maxPrice !== null && tempFilters.maxPrice > 0) {
            priceDisplay.innerText = '≤ RM ' + tempFilters.maxPrice;
        } else {
            priceDisplay.innerText = 'Any Price';
        }
    }

    var count = 0;
    var total = 0;
    for (var i = 0; i < (landlordMarkers || []).length; i++) {
        var item = landlordMarkers[i];
        if (!item) continue;
        var isOwner = currentUser && currentUser.id === item.user_id;
        var isAdmin = currentUser && currentUser.role === 'admin';
        var isVerified = item.is_verified === 1;
        if (!isVerified && !isAdmin && !isOwner) continue;

        total++;
        if (propertyMatchesFilters(item, tempFilters)) {
            count++;
        }
    }

    var applyBtn = document.getElementById('filter-apply-btn');
    if (applyBtn) {
        if (hasActiveFilter(tempFilters)) {
            applyBtn.innerText = 'Show ' + count + ' Properties';
        } else {
            applyBtn.innerText = 'Show All (' + total + ')';
        }
    }
}

function handleApplyFilters(event) {
    if (event) event.preventDefault();
    activeFilters = getFormFilterValues();
    closeFilterModal();
    applyFiltersToMap();
}

function resetAllFilters(skipMapRefresh) {
    activeFilters = {
        maxPrice: null,
        roomTypes: [],
        bathroomType: '',
        utilities: [],
        floorLevels: [],
        generalPrefs: [],
        occupationPrefs: []
    };
    syncFilterFormWithActive();
    onFilterCriteriaChanged();
    if (skipMapRefresh) {
        applyFiltersToMap();
    }
}

function applyFiltersToMap() {
    var isFiltered = hasActiveFilter(activeFilters);
    var visibleCount = 0;
    var totalCount = 0;

    for (var i = 0; i < (landlordMarkers || []).length; i++) {
        var item = landlordMarkers[i];
        if (!item || !item.marker) continue;

        var isOwner = currentUser && currentUser.id === item.user_id;
        var isAdmin = currentUser && currentUser.role === 'admin';
        var isVerified = item.is_verified === 1;

        if (!isVerified && !isAdmin && !isOwner) {
            if (map.hasLayer(item.marker)) map.removeLayer(item.marker);
            continue;
        }

        totalCount++;
        var matches = propertyMatchesFilters(item, activeFilters);

        if (matches) {
            visibleCount++;
            if (!map.hasLayer(item.marker)) {
                map.addLayer(item.marker);
            }
        } else {
            if (map.hasLayer(item.marker)) {
                map.removeLayer(item.marker);
            }
            if (item.marker.isPopupOpen && item.marker.isPopupOpen()) {
                item.marker.closePopup();
            }
        }
    }

    var count = countActiveFilterCriteria(activeFilters);
    var filterBtn = document.getElementById('search-filter-btn');
    var badge = document.getElementById('filter-active-count');
    var banner = document.getElementById('active-filter-banner');
    var bannerSummary = document.getElementById('active-filter-summary');

    if (isFiltered) {
        if (filterBtn) filterBtn.classList.add('active');
        if (badge) {
            badge.style.display = 'inline-flex';
            badge.innerText = count;
        }
        if (banner) {
            banner.style.display = 'flex';
            if (bannerSummary) {
                bannerSummary.innerHTML = 'Showing <b>' + visibleCount + '</b> of ' + totalCount + ' properties';
            }
        }
    } else {
        if (filterBtn) filterBtn.classList.remove('active');
        if (badge) badge.style.display = 'none';
        if (banner) banner.style.display = 'none';
    }

    var searchInput = document.getElementById('search-input');
    if (searchInput && searchInput.value.trim()) {
        performSearch();
    }
}

// 4. Unified Search Bar Functions (Properties & Kuching Locations)
function clearSearch() {
    var searchInput = document.getElementById("search-input");
    var resultsContainer = document.getElementById("search-results");
    var searchBox = document.getElementById("search-box");
    var clearBtn = document.getElementById("search-clear-btn");
    if (searchInput) searchInput.value = '';
    if (resultsContainer) {
        resultsContainer.innerHTML = '';
        resultsContainer.style.display = 'none';
    }
    if (searchBox) searchBox.classList.remove('has-results');
    if (clearBtn) clearBtn.style.display = 'none';
}

function performSearch() {
    var searchInput = document.getElementById("search-input");
    var query = searchInput ? searchInput.value.trim() : '';
    var resultsContainer = document.getElementById("search-results");
    var searchBox = document.getElementById("search-box");
    var clearBtn = document.getElementById("search-clear-btn");

    if (clearBtn) {
        clearBtn.style.display = query ? 'inline-flex' : 'none';
    }

    if (!query) {
        if (resultsContainer) {
            resultsContainer.innerHTML = '';
            resultsContainer.style.display = 'none';
        }
        if (searchBox) searchBox.classList.remove('has-results');
        return;
    }

    resultsContainer.innerHTML = '<div class="result-feedback"><span style="display:inline-block; animation:spin 1s linear infinite; margin-right:6px;">🔄</span> Searching properties & places in Kuching...</div>';
    resultsContainer.style.display = 'block';
    if (searchBox) searchBox.classList.add('has-results');

    var qLower = query.toLowerCase();
    var qWords = qLower.split(/\s+/).filter(Boolean);

    // 1. Search registered rental property listings
    var matchedProperties = (landlordMarkers || []).filter(function (prop) {
        if (!prop) return false;
        var isOwner = currentUser && currentUser.id === prop.user_id;
        var isAdmin = currentUser && currentUser.role === 'admin';
        if (prop.is_verified !== 1 && !isAdmin && !isOwner) {
            return false;
        }

        if (typeof propertyMatchesFilters === 'function' && !propertyMatchesFilters(prop, activeFilters)) {
            return false;
        }

        var name = (prop.name || '').toLowerCase();
        var desc = (prop.desc || '').toLowerCase();
        var landlord = (prop.landlord_name || '').toLowerCase();
        var price = (prop.price ? String(prop.price) : '').toLowerCase();
        var detailsStr = '';
        if (prop.details) {
            if (typeof prop.details === 'string') {
                detailsStr = prop.details.toLowerCase();
            } else {
                try { detailsStr = JSON.stringify(prop.details).toLowerCase(); } catch (e) { }
            }
        }

        if (name.includes(qLower) || desc.includes(qLower) || landlord.includes(qLower) || price.includes(qLower) || detailsStr.includes(qLower)) {
            return true;
        }
        if (qWords.length > 1) {
            var allWords = qWords.every(function (w) {
                return name.includes(w) || desc.includes(w) || landlord.includes(w) || detailsStr.includes(w);
            });
            if (allWords) return true;
        }
        return false;
    });

    // 2. Search OpenStreetMap Nominatim for Kuching geographical places
    var queryFormatted = query;
    if (!queryFormatted.toLowerCase().includes('kuching')) {
        queryFormatted += ', Kuching, Sarawak';
    }

    var nominatimUrl = 'https://nominatim.openstreetmap.org/search?format=json&q=' + encodeURIComponent(queryFormatted) +
        '&countrycodes=my&viewbox=109.80,1.85,110.70,1.15&bounded=1&limit=5';

    fetch(nominatimUrl)
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            var localPlaces = (data || []).filter(function (item) {
                var lat = parseFloat(item.lat);
                var lon = parseFloat(item.lon);
                return (typeof isInsideKuchingBoundary === 'function') ? isInsideKuchingBoundary(lat, lon) : true;
            });

            renderSearchResults(query, matchedProperties, localPlaces);
        })
        .catch(function (error) {
            console.error('Search geocoding error:', error);
            renderSearchResults(query, matchedProperties, []);
        });
}

function renderSearchResults(query, properties, places) {
    var resultsContainer = document.getElementById("search-results");
    var searchBox = document.getElementById("search-box");
    if (!resultsContainer) return;

    resultsContainer.innerHTML = '';

    var totalCount = properties.length + places.length;
    if (totalCount === 0) {
        var emptyDiv = document.createElement('div');
        emptyDiv.className = 'result-feedback result-empty';
        emptyDiv.innerHTML = '<div style="font-weight:600; margin-bottom:4px; color:#1e293b;">No results found</div>' +
            '<div style="font-size:12.5px; color:#64748b;">No properties or locations match "<b>' + escapeHtml(query) + '</b>" in Kuching.</div>';
        resultsContainer.appendChild(emptyDiv);
        return;
    }

    // Render Property Listings Group
    if (properties.length > 0) {
        var propHeader = document.createElement('div');
        propHeader.className = 'search-category-header';
        propHeader.innerHTML = '<span>🏠 Rental Properties (' + properties.length + ')</span>';
        resultsContainer.appendChild(propHeader);

        properties.forEach(function (prop) {
            var div = document.createElement('div');
            div.className = 'result-item';

            var verifiedTag = prop.is_verified === 1
                ? '<svg class="verified-seal-icon" width="15" height="15" viewBox="0 0 24 24" fill="none" title="Polisewa Approved"><path fill="#10B981" d="M12 1L15.39 4.39L20.18 4.39L20.18 9.18L23.57 12.57L20.18 15.96L20.18 20.75L15.39 20.75L12 24.14L8.61 20.75L3.82 20.75L3.82 15.96L0.43 12.57L3.82 9.18L3.82 4.39L8.61 4.39L12 1Z"/><path stroke="#ffffff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" d="M8.5 12.5L11 15L16.5 9.5"/></svg>'
                : '<span style="font-size:10px;font-weight:700;color:#d97706;background:#fef3c7;padding:1px 6px;border-radius:4px;border:1px solid #fde68a;">Pending</span>';
            var priceTag = prop.price ? '<span class="result-price-badge">RM ' + escapeHtml(prop.price) + '/mo</span>' : '';
            var descSnippet = prop.desc ? escapeHtml(prop.desc) : 'No description';
            var landlordTag = prop.landlord_name ? ' • 🔑 ' + escapeHtml(prop.landlord_name) : '';

            var dObj = (typeof parsePropertyDetails === 'function') ? parsePropertyDetails(prop.details) : null;
            var chipsHtml = '';
            if (dObj) {
                var chips = [];
                if (dObj.room_type) chips.push('🛏️ ' + escapeHtml(dObj.room_type));
                if (dObj.bathroom_type) chips.push('🚿 ' + escapeHtml(dObj.bathroom_type));
                if (dObj.utilities && Array.isArray(dObj.utilities) && dObj.utilities.length > 0) {
                    for (var cu = 0; cu < Math.min(dObj.utilities.length, 2); cu++) {
                        var cuName = dObj.utilities[cu].replace(' / Internet Access', '').replace('Air-Conditioning', 'Air-Con');
                        chips.push('✓ ' + escapeHtml(cuName));
                    }
                }
                if (chips.length > 0) {
                    chipsHtml = '<div class="result-features-preview">' +
                        chips.map(function (c) { return '<span class="result-feature-chip">' + c + '</span>'; }).join('') +
                        '</div>';
                }
            }

            div.innerHTML = '<div class="result-icon">🏠</div>' +
                '<div class="result-text">' +
                '<div class="result-title">' +
                '<div class="result-title-left">' +
                '<span class="result-name">' + escapeHtml(prop.name || 'Rental Property') + '</span>' +
                verifiedTag +
                '</div>' +
                priceTag +
                '</div>' +
                '<div class="result-sub">' + descSnippet + landlordTag + '</div>' +
                chipsHtml +
                '</div>';

            div.onclick = function () {
                map.flyTo([prop.lat, prop.lng], 16, { animate: true, duration: 1.0 });
                resultsContainer.style.display = 'none';
                if (searchBox) searchBox.classList.remove('has-results');
                document.getElementById("search-input").value = prop.name || '';
                var clearBtn = document.getElementById("search-clear-btn");
                if (clearBtn) clearBtn.style.display = 'inline-flex';

                setTimeout(function () {
                    if (prop.marker) {
                        prop.marker.openPopup();
                    }
                }, 450);
            };

            resultsContainer.appendChild(div);
        });
    }

    // Render Kuching Places Group
    if (places.length > 0) {
        var placeHeader = document.createElement('div');
        placeHeader.className = 'search-category-header';
        placeHeader.innerHTML = '<span>📍 Kuching Locations (' + places.length + ')</span>';
        resultsContainer.appendChild(placeHeader);

        places.forEach(function (item) {
            var div = document.createElement('div');
            div.className = 'result-item';

            var parts = item.display_name.split(',').map(function (s) { return s.trim(); });
            var mainTitle = parts[0] || item.display_name;
            var subTitle = parts.slice(1, 4).join(', ');

            div.innerHTML = '<div class="result-icon">📍</div>' +
                '<div class="result-text">' +
                '<div class="result-title">' + escapeHtml(mainTitle) + '</div>' +
                '<div class="result-sub">' + escapeHtml(subTitle) + '</div>' +
                '</div>';

            div.onclick = function () {
                var lat = parseFloat(item.lat);
                var lon = parseFloat(item.lon);

                map.flyTo([lat, lon], 16, { animate: true, duration: 1.0 });

                if (window.searchLocationMarker) {
                    map.removeLayer(window.searchLocationMarker);
                }

                var locationIcon = L.divIcon({
                    className: 'custom-div-icon',
                    html: '<div class="marker-pin" style="background:#2563eb;"></div><span>📍</span>',
                    iconSize: [30, 30],
                    iconAnchor: [15, 30],
                    popupAnchor: [0, -30]
                });

                window.searchLocationMarker = L.marker([lat, lon], { icon: locationIcon }).addTo(map);
                window.searchLocationMarker.bindPopup("<b>" + escapeHtml(mainTitle) + "</b><br><small>" + escapeHtml(subTitle) + "</small>").openPopup();

                resultsContainer.style.display = 'none';
                if (searchBox) searchBox.classList.remove('has-results');
                document.getElementById("search-input").value = mainTitle;
                var clearBtn = document.getElementById("search-clear-btn");
                if (clearBtn) clearBtn.style.display = 'inline-flex';
            };

            resultsContainer.appendChild(div);
        });
    }
}

// 5. Search Bar Input Event Listeners
document.addEventListener('DOMContentLoaded', function () {
    var searchInput = document.getElementById("search-input");
    var searchButton = document.getElementById("search-button");

    if (searchInput) {
        searchInput.addEventListener("input", function () {
            var val = searchInput.value.trim();
            var clearBtn = document.getElementById("search-clear-btn");
            if (clearBtn) clearBtn.style.display = val ? 'inline-flex' : 'none';

            if (searchDebounceTimer) clearTimeout(searchDebounceTimer);

            if (!val) {
                clearSearch();
                return;
            }

            searchDebounceTimer = setTimeout(function () {
                performSearch();
            }, 250);
        });

        searchInput.addEventListener("keydown", function (e) {
            if (e.key === "Enter") {
                if (searchDebounceTimer) clearTimeout(searchDebounceTimer);
                performSearch();
            }
        });
    }

    if (searchButton) {
        searchButton.addEventListener("click", function () {
            if (searchDebounceTimer) clearTimeout(searchDebounceTimer);
            performSearch();
        });
    }
});
