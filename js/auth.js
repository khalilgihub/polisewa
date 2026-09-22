/**
 * PoliSewa - Authentication & User Session Module (js/auth.js)
 * Manages user accounts, signin/signup, OTP verification, delete account & session state.
 */

var currentUser = null;
try {
    currentUser = JSON.parse(localStorage.getItem('polisewa_user') || 'null');
} catch (e) {
    currentUser = null;
}

var activeRole = 'student';
var activeForm = 'signin';
var otpTimerInterval = null;

// DOM Elements
var authBtn = document.getElementById("auth-btn");
var authModalOverlay = document.getElementById("auth-modal-overlay");
var authDropdown = document.getElementById("auth-dropdown");
var deleteModalOverlay = document.getElementById("delete-modal-overlay");
var adminModalOverlay = document.getElementById("admin-modal-overlay");
var filterModalOverlay = document.getElementById("filter-modal-overlay");

// String escaping helper for XSS prevention
function escapeHtml(str) {
    if (!str) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

// 1. Force Logout Handler
function forceLogout(reason) {
    if (!currentUser && !localStorage.getItem('polisewa_user')) return;
    currentUser = null;
    localStorage.removeItem('polisewa_user');
    if (authDropdown) authDropdown.classList.remove('active');
    if (adminModalOverlay) adminModalOverlay.classList.remove('active');
    if (deleteModalOverlay) deleteModalOverlay.classList.remove('active');
    updateAuthButton();
    if (typeof loadProperties === 'function') {
        loadProperties();
    }
    if (reason) {
        setTimeout(function () {
            alert(reason);
        }, 100);
    }
}

// 2. Verify user session with server
var isVerifyingSession = false;
function verifyUserSession(session) {
    if (!session || !session.id || isVerifyingSession) return;
    isVerifyingSession = true;
    var verifyUrl = '/api/auth/verify?user_id=' + encodeURIComponent(session.id);
    if (session.email) {
        verifyUrl += '&email=' + encodeURIComponent(session.email);
    }

    fetch(verifyUrl)
        .then(function (res) {
            if (res.status === 401 || res.status === 404) {
                forceLogout('Your account has been deleted or is no longer active.');
                return null;
            }
            return res.json();
        })
        .then(function (data) {
            isVerifyingSession = false;
            if (data && data.user) {
                currentUser = data.user;
                localStorage.setItem('polisewa_user', JSON.stringify(data.user));
                updateAuthButton();
            }
        })
        .catch(function () {
            isVerifyingSession = false;
        });
}

// 3. Update Auth Button & Navigation UI
function updateAuthButton() {
    var btn = document.getElementById("auth-btn");
    var adminBtn = document.getElementById("auth-admin-btn");
    var deleteDivider = document.getElementById("auth-delete-divider");
    var deleteBtn = document.getElementById("auth-delete-btn");

    if (!btn) return;

    if (currentUser) {
        var roleBadge = (currentUser.role === 'admin') ? '🛡️' : (currentUser.role === 'landlord') ? '🔑' : '🎓';
        var displayName = currentUser.name ? currentUser.name.split(' ')[0] : 'User';
        btn.innerHTML = '<span class="auth-role-badge">' + roleBadge + '</span> ' + escapeHtml(displayName) +
            ' <svg class="auth-chevron" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"></polyline></svg>';
        btn.classList.add("logged-in");

        if (currentUser.role === 'admin') {
            if (adminBtn) adminBtn.style.display = 'flex';
            if (deleteDivider) deleteDivider.style.display = 'none';
            if (deleteBtn) deleteBtn.style.display = 'none';
        } else {
            if (adminBtn) adminBtn.style.display = 'none';
            if (deleteDivider) deleteDivider.style.display = 'block';
            if (deleteBtn) deleteBtn.style.display = 'flex';
        }
    } else {
        btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg><span class="auth-btn-text">Login / Sign Up</span>';
        btn.classList.remove("logged-in");
        if (authDropdown) authDropdown.classList.remove("active");
        if (adminBtn) adminBtn.style.display = 'none';
        if (deleteDivider) deleteDivider.style.display = 'none';
        if (deleteBtn) deleteBtn.style.display = 'none';
    }
}

// 4. Modal Role & Form Controls
function setRole(role) {
    activeRole = role;
    var tabs = document.querySelectorAll('.role-tab');
    tabs.forEach(function (tab) {
        tab.classList.remove('active');
        if (tab.innerText.toLowerCase().includes(role)) {
            tab.classList.add('active');
        }
    });

    var phoneGroup = document.getElementById('phone-input-group');
    var signupPhone = document.getElementById('signup-phone');
    if (phoneGroup && signupPhone) {
        if (role === 'landlord') {
            phoneGroup.style.display = 'block';
            signupPhone.required = true;
        } else {
            phoneGroup.style.display = 'none';
            signupPhone.required = false;
        }
    }
}

function setFormType(type) {
    activeForm = type;
    var tabs = document.querySelectorAll('.toggle-tab');
    tabs.forEach(function (tab) {
        tab.classList.remove('active');
        if (tab.innerText.toLowerCase().includes(type === 'signin' ? 'sign in' : 'sign up')) {
            tab.classList.add('active');
        }
    });

    var signinForm = document.getElementById('signin-form');
    var signupForm = document.getElementById('signup-form');
    var otpSection = document.getElementById('otp-verification-section');

    if (otpSection) otpSection.style.display = 'none';

    if (type === 'signin') {
        if (signinForm) signinForm.classList.add('active');
        if (signupForm) signupForm.classList.remove('active');
    } else {
        if (signinForm) signinForm.classList.remove('active');
        if (signupForm) signupForm.classList.add('active');
    }
}

function openAuthModal() {
    if (authDropdown) authDropdown.classList.remove('active');
    if (authModalOverlay) authModalOverlay.classList.add('active');
    setFormType('signin');
}

function closeAuthModal() {
    if (authModalOverlay) authModalOverlay.classList.remove('active');
}

function backToAuthForm() {
    var otpSection = document.getElementById('otp-verification-section');
    var normalAuthForms = document.getElementById('normal-auth-forms');
    if (otpSection) otpSection.style.display = 'none';
    if (normalAuthForms) normalAuthForms.style.display = 'block';
    setFormType(activeForm);
}

// 5. Form Submissions & OTP
function handleAuthSubmit(event, type) {
    event.preventDefault();
    var submitBtn = event.target.querySelector('.submit-btn');
    var originalText = submitBtn.innerText;
    submitBtn.disabled = true;
    submitBtn.innerText = 'Please wait...';

    if (type === 'signin') {
        var email = document.getElementById('signin-email').value.trim();
        var password = document.getElementById('signin-password').value;

        fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, password: password })
        })
            .then(function (res) { return res.json().then(function (d) { if (!res.ok) throw new Error(d.error || 'Login failed'); return d; }); })
            .then(function (data) {
                currentUser = data.user;
                localStorage.setItem('polisewa_user', JSON.stringify(currentUser));
                updateAuthButton();
                closeAuthModal();
                if (typeof loadProperties === 'function') loadProperties();
                alert('Welcome back, ' + currentUser.name + '!');
            })
            .catch(function (err) {
                alert(err.message);
            })
            .finally(function () {
                submitBtn.disabled = false;
                submitBtn.innerText = originalText;
            });

    } else if (type === 'signup') {
        var name = document.getElementById('signup-name').value.trim();
        var emailVal = document.getElementById('signup-email').value.trim();
        var pass = document.getElementById('signup-password').value;
        var phone = document.getElementById('signup-phone').value.trim();

        fetch('/api/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: name, email: emailVal, password: pass, role: activeRole, phone: phone })
        })
            .then(function (res) { return res.json().then(function (d) { if (!res.ok) throw new Error(d.error || 'Registration failed'); return d; }); })
            .then(function (data) {
                if (data.requiresOtp) {
                    showOtpSection(data.email || emailVal);
                } else {
                    currentUser = data.user;
                    localStorage.setItem('polisewa_user', JSON.stringify(currentUser));
                    updateAuthButton();
                    closeAuthModal();
                    if (typeof loadProperties === 'function') loadProperties();
                    alert('Registration successful! Welcome to PoliSewa, ' + currentUser.name + '!');
                }
            })
            .catch(function (err) {
                alert(err.message);
            })
            .finally(function () {
                submitBtn.disabled = false;
                submitBtn.innerText = originalText;
            });
    }
}

function showOtpSection(email) {
    var normalAuthForms = document.getElementById('normal-auth-forms');
    var otpSection = document.getElementById('otp-verification-section');
    var targetEmailSpan = document.getElementById('otp-target-email');

    if (normalAuthForms) normalAuthForms.style.display = 'none';
    if (otpSection) otpSection.style.display = 'block';
    if (targetEmailSpan) targetEmailSpan.innerText = email;

    // Reset OTP boxes
    var otpDigits = document.querySelectorAll('.otp-digit');
    otpDigits.forEach(function (input) { input.value = ''; });
    if (otpDigits[0]) otpDigits[0].focus();

    startOtpTimer(60);
}

function initOtpInputs() {
    var otpDigits = document.querySelectorAll('.otp-digit');
    otpDigits.forEach(function (input, idx) {
        input.addEventListener('input', function (e) {
            var val = e.target.value.replace(/[^0-9]/g, '');
            e.target.value = val ? val.slice(-1) : '';
            if (val && idx < otpDigits.length - 1) {
                otpDigits[idx + 1].focus();
            }
        });

        input.addEventListener('keydown', function (e) {
            if (e.key === 'Backspace' && !e.target.value && idx > 0) {
                otpDigits[idx - 1].focus();
            }
        });

        input.addEventListener('paste', function (e) {
            e.preventDefault();
            var pasteData = (e.clipboardData || window.clipboardData).getData('text').trim().replace(/[^0-9]/g, '');
            if (!pasteData) return;
            var chars = pasteData.slice(0, 6).split('');
            chars.forEach(function (ch, i) {
                if (otpDigits[i]) otpDigits[i].value = ch;
            });
            var nextIndex = Math.min(chars.length, otpDigits.length - 1);
            if (otpDigits[nextIndex]) otpDigits[nextIndex].focus();
        });
    });
}

function handleVerifyOtp() {
    var otpDigits = document.querySelectorAll('.otp-digit');
    var otpCode = '';
    otpDigits.forEach(function (inp) { otpCode += inp.value.trim(); });

    var email = document.getElementById('otp-target-email').innerText.trim();

    if (otpCode.length < 6) {
        alert('Please enter the complete 6-digit verification code.');
        return;
    }

    var verifyBtn = document.getElementById('otp-verify-btn');
    var originalText = verifyBtn.innerText;
    verifyBtn.disabled = true;
    verifyBtn.innerText = 'Verifying...';

    fetch('/api/auth/verify-otp', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email, otp: otpCode })
    })
        .then(function (res) { return res.json().then(function (d) { if (!res.ok) throw new Error(d.error || 'Verification failed'); return d; }); })
        .then(function (data) {
            currentUser = data.user;
            localStorage.setItem('polisewa_user', JSON.stringify(currentUser));
            updateAuthButton();
            closeAuthModal();
            if (typeof loadProperties === 'function') loadProperties();
            alert('Email verified successfully! Welcome to PoliSewa, ' + currentUser.name + '!');
        })
        .catch(function (err) {
            alert(err.message);
        })
        .finally(function () {
            verifyBtn.disabled = false;
            verifyBtn.innerText = originalText;
        });
}

function handleResendOtp() {
    var email = document.getElementById('otp-target-email').innerText.trim();
    var resendBtn = document.getElementById('otp-resend-btn');
    if (resendBtn) resendBtn.disabled = true;

    fetch('/api/auth/resend-otp', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email })
    })
        .then(function (res) { return res.json().then(function (d) { if (!res.ok) throw new Error(d.error || 'Failed to resend code'); return d; }); })
        .then(function () {
            alert('A new verification code has been sent to ' + email + '.');
            startOtpTimer(60);
        })
        .catch(function (err) {
            alert(err.message);
            if (resendBtn) resendBtn.disabled = false;
        });
}

function startOtpTimer(durationSeconds) {
    if (otpTimerInterval) clearInterval(otpTimerInterval);
    var timerText = document.getElementById('otp-timer-text');
    var resendBtn = document.getElementById('otp-resend-btn');
    var timeLeft = durationSeconds;

    if (resendBtn) resendBtn.style.display = 'none';
    if (timerText) {
        timerText.style.display = 'inline';
        timerText.innerText = 'Resend in ' + timeLeft + 's';
    }

    otpTimerInterval = setInterval(function () {
        timeLeft--;
        if (timeLeft <= 0) {
            clearInterval(otpTimerInterval);
            if (timerText) timerText.style.display = 'none';
            if (resendBtn) {
                resendBtn.style.display = 'inline';
                resendBtn.disabled = false;
            }
        } else {
            if (timerText) timerText.innerText = 'Resend in ' + timeLeft + 's';
        }
    }, 1000);
}

// 6. Logout & Delete Account
function handleLogout() {
    currentUser = null;
    localStorage.removeItem('polisewa_user');
    if (authDropdown) authDropdown.classList.remove('active');
    updateAuthButton();
    if (typeof loadProperties === 'function') loadProperties();
}

function openDeleteAccountModal() {
    if (authDropdown) authDropdown.classList.remove('active');
    var passInp = document.getElementById('delete-password');
    if (passInp) passInp.value = '';
    if (deleteModalOverlay) deleteModalOverlay.classList.add('active');
}

function closeDeleteAccountModal() {
    if (deleteModalOverlay) deleteModalOverlay.classList.remove('active');
}

function handleDeleteAccount() {
    if (!currentUser) return;
    var password = document.getElementById('delete-password').value;
    if (!password) {
        alert('Please enter your password to confirm account deletion.');
        return;
    }

    var delBtn = document.getElementById('delete-confirm-btn');
    delBtn.disabled = true;
    delBtn.innerText = 'Deleting...';

    fetch('/api/auth/delete-account', {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: currentUser.id, password: password })
    })
        .then(function (res) { return res.json().then(function (d) { if (!res.ok) throw new Error(d.error || 'Failed to delete account'); return d; }); })
        .then(function () {
            alert('Your account and all associated properties have been permanently deleted.');
            closeDeleteAccountModal();
            handleLogout();
        })
        .catch(function (err) {
            alert(err.message);
        })
        .finally(function () {
            delBtn.disabled = false;
            delBtn.innerText = 'Delete Forever';
        });
}

// 7. Global Event Listeners (Auth button toggle, outside clicks, escape key)
document.addEventListener('DOMContentLoaded', function () {
    updateAuthButton();
    initOtpInputs();
    if (currentUser) {
        verifyUserSession(currentUser);
    }
});

if (authBtn) {
    authBtn.onclick = function (e) {
        e.stopPropagation();
        if (currentUser) {
            if (authDropdown) authDropdown.classList.toggle('active');
        } else {
            openAuthModal();
        }
    };
}

if (authModalOverlay) {
    authModalOverlay.onclick = function (e) {
        if (e.target === authModalOverlay) closeAuthModal();
    };
}

if (deleteModalOverlay) {
    deleteModalOverlay.onclick = function (e) {
        if (e.target === deleteModalOverlay) closeDeleteAccountModal();
    };
}

// Keyboard Navigation & Outside click listeners
document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
        var searchBox = document.getElementById('search-box');
        var resultsContainer = document.getElementById('search-results');
        if (resultsContainer && resultsContainer.style.display === 'block') {
            resultsContainer.style.display = 'none';
            if (searchBox) searchBox.classList.remove('has-results');
        }
        if (typeof closePropertyPanel === 'function') {
            var panel = document.getElementById('property-panel');
            if (panel && panel.classList.contains('active')) closePropertyPanel();
        }
        if (authModalOverlay && authModalOverlay.classList.contains('active')) closeAuthModal();
        if (deleteModalOverlay && deleteModalOverlay.classList.contains('active')) closeDeleteAccountModal();
        if (adminModalOverlay && adminModalOverlay.classList.contains('active') && typeof closeAdminDashboardModal === 'function') closeAdminDashboardModal();
        if (filterModalOverlay && filterModalOverlay.classList.contains('active') && typeof closeFilterModal === 'function') closeFilterModal();
        if (authDropdown && authDropdown.classList.contains('active')) authDropdown.classList.remove('active');
    }
});

document.addEventListener('click', function (e) {
    var searchBox = document.getElementById("search-box");
    var resultsContainer = document.getElementById("search-results");
    if (searchBox && !searchBox.contains(e.target)) {
        if (resultsContainer) resultsContainer.style.display = 'none';
        searchBox.classList.remove('has-results');
    }
    if (authDropdown && !authDropdown.contains(e.target) && e.target !== authBtn && (!authBtn || !authBtn.contains(e.target))) {
        authDropdown.classList.remove('active');
    }
});
