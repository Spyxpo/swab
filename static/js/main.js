document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('build-form');
    const buildButton = document.getElementById('build-button');
    const buildProgress = document.getElementById('build-progress');
    const buildComplete = document.getElementById('build-complete');
    const progressFill = document.getElementById('progress-fill');
    const progressPercent = document.getElementById('progress-percent');
    const progressMessage = document.getElementById('progress-message');
    const downloadLinks = document.getElementById('download-links');
    const webUrlInput = document.getElementById('web-url');
    const previewIframe = document.getElementById('preview-iframe');
    const placeholderContent = document.getElementById('placeholder-content');
    const deviceFrame = document.getElementById('device-frame');
    const deviceButtons = document.querySelectorAll('.device-btn');
    const keystoreSection = document.getElementById('keystore-section');
    const platformSelect = document.getElementById('platform-select');
    const keystoreFile = document.getElementById('keystore-file');
    const keystoreDetails = document.getElementById('keystore-details');
    const keystoreUploadLabel = document.getElementById('keystore-upload-label');

    // Project save/open elements
    const saveProjectBtn = document.getElementById('save-project-btn');
    const openProjectBtn = document.getElementById('open-project-btn');
    const openProjectFile = document.getElementById('open-project-file');

    // Store paths for icon and keystore (set after upload)
    let currentIconPath = null;
    let currentKeystorePath = null;

    // Center progress elements
    const centerProgress = document.getElementById('center-progress');
    const centerProgressFill = document.getElementById('center-progress-fill');
    const centerProgressText = document.getElementById('center-progress-text');
    const platformDropdownWrapper = document.querySelector('.platform-dropdown-wrapper');

    // Settings dialog elements
    const settingsBtn = document.getElementById('settings-btn');
    const settingsOverlay = document.getElementById('settings-overlay');
    const settingsClose = document.getElementById('settings-close');
    const settingsCancel = document.getElementById('settings-cancel');
    const settingsSave = document.getElementById('settings-save');

    // Icon upload elements
    const iconFile = document.getElementById('icon-file');
    const iconPreview = document.getElementById('icon-preview');
    const iconUploadLabel = document.getElementById('icon-upload-label');

    // Mapping between hidden form checkboxes and settings dialog checkboxes
    const settingsMapping = {
        'allow-zoom': 'setting-allow-zoom',
        'enable-javascript': 'setting-enable-javascript',
        'enable-dom-storage': 'setting-enable-dom-storage',
        'enable-geolocation': 'setting-enable-geolocation',
        'enable-pull-refresh': 'setting-enable-pull-refresh',
        'show-navigation': 'setting-show-navigation',
        'enable-file-access': 'setting-enable-file-access',
        'enable-cache': 'setting-enable-cache',
        'enable-media-autoplay': 'setting-enable-media-autoplay'
    };

    // Settings dialog handlers
    settingsBtn.addEventListener('click', openSettingsDialog);
    settingsClose.addEventListener('click', closeSettingsDialog);
    settingsCancel.addEventListener('click', closeSettingsDialog);
    settingsSave.addEventListener('click', saveSettings);
    settingsOverlay.addEventListener('click', function(e) {
        if (e.target === settingsOverlay) {
            closeSettingsDialog();
        }
    });

    function openSettingsDialog() {
        // Sync dialog checkboxes with hidden form checkboxes
        for (const [formId, dialogId] of Object.entries(settingsMapping)) {
            const formCheckbox = document.getElementById(formId);
            const dialogCheckbox = document.getElementById(dialogId);
            if (formCheckbox && dialogCheckbox) {
                dialogCheckbox.checked = formCheckbox.checked;
            }
        }
        settingsOverlay.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }

    function closeSettingsDialog() {
        settingsOverlay.style.display = 'none';
        document.body.style.overflow = '';
    }

    function saveSettings() {
        // Sync hidden form checkboxes with dialog checkboxes
        for (const [formId, dialogId] of Object.entries(settingsMapping)) {
            const formCheckbox = document.getElementById(formId);
            const dialogCheckbox = document.getElementById(dialogId);
            if (formCheckbox && dialogCheckbox) {
                formCheckbox.checked = dialogCheckbox.checked;
            }
        }
        closeSettingsDialog();
        showToast('Settings saved', 'success');
    }

    // Close dialog on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && settingsOverlay.style.display === 'flex') {
            closeSettingsDialog();
        }
    });

    // Handle platform selection for keystore visibility
    platformSelect.addEventListener('change', function() {
        const selectedPlatform = this.value;
        const isAndroid = selectedPlatform === 'android' || selectedPlatform === 'android_aab';
        keystoreSection.style.display = isAndroid ? 'block' : 'none';
    });

    // Handle icon file selection
    iconFile.addEventListener('change', function() {
        if (this.files && this.files.length > 0) {
            const file = this.files[0];
            const reader = new FileReader();

            reader.onload = function(e) {
                iconPreview.innerHTML = `<img src="${e.target.result}" alt="App Icon">`;
                iconPreview.classList.add('has-icon');
            };

            reader.readAsDataURL(file);

            iconUploadLabel.innerHTML = `
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M22 11.08V12a10 10 0 11-5.93-9.14"/>
                    <polyline points="22 4 12 14.01 9 11.01"/>
                </svg>
                <span>Change Icon</span>
            `;
        }
    });

    // Handle keystore file selection
    keystoreFile.addEventListener('change', function() {
        if (this.files && this.files.length > 0) {
            const fileName = this.files[0].name;
            keystoreUploadLabel.innerHTML = `
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M22 11.08V12a10 10 0 11-5.93-9.14"/>
                    <polyline points="22 4 12 14.01 9 11.01"/>
                </svg>
                <span>${fileName}</span>
                <small class="hint">Click to change file</small>
            `;
            keystoreUploadLabel.style.borderColor = 'var(--success)';
            keystoreUploadLabel.style.background = 'var(--success-bg)';
            keystoreDetails.style.display = 'block';
        } else {
            resetKeystoreUpload();
        }
    });

    function resetKeystoreUpload() {
        keystoreUploadLabel.innerHTML = `
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M17 8l-5-5-5 5M12 3v12"/>
            </svg>
            <span>Click to upload or drag and drop</span>
            <small class="hint">.jks or .keystore file</small>
        `;
        keystoreUploadLabel.style.borderColor = '';
        keystoreUploadLabel.style.background = '';
        keystoreDetails.style.display = 'none';
    }

    // Handle URL input for preview
    let debounceTimer;
    webUrlInput.addEventListener('input', function() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            updatePreview(this.value);
        }, 500);
    });

    function updatePreview(url) {
        if (url && isValidUrl(url)) {
            placeholderContent.style.display = 'none';
            previewIframe.style.display = 'block';
            previewIframe.src = url;
        } else {
            placeholderContent.style.display = 'flex';
            previewIframe.style.display = 'none';
            previewIframe.src = '';
        }
    }

    function isValidUrl(string) {
        try {
            const url = new URL(string);
            return url.protocol === 'http:' || url.protocol === 'https:';
        } catch (_) {
            return false;
        }
    }

    // Handle device selection
    deviceButtons.forEach(button => {
        button.addEventListener('click', function() {
            deviceButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            const device = this.dataset.device;
            deviceFrame.className = 'device-frame ' + device;
        });
    });

    // Handle form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const selectedPlatform = platformSelect.value;

        // Validate platform selection
        if (!selectedPlatform) {
            showToast('Please select a target platform', 'error');
            return;
        }

        // Collect form data
        const formData = {
            app_name: document.getElementById('app-name').value,
            app_description: document.getElementById('app-description').value,
            app_version: document.getElementById('app-version').value,
            build_number: document.getElementById('build-number').value,
            package_name: document.getElementById('package-name').value,
            web_url: document.getElementById('web-url').value,
            platforms: [selectedPlatform],
            // WebView feature options from hidden checkboxes
            allow_zoom: document.getElementById('allow-zoom').checked,
            enable_javascript: document.getElementById('enable-javascript').checked,
            enable_dom_storage: document.getElementById('enable-dom-storage').checked,
            enable_geolocation: document.getElementById('enable-geolocation').checked,
            enable_pull_refresh: document.getElementById('enable-pull-refresh').checked,
            show_navigation: document.getElementById('show-navigation').checked,
            enable_file_access: document.getElementById('enable-file-access').checked,
            enable_cache: document.getElementById('enable-cache').checked,
            enable_media_autoplay: document.getElementById('enable-media-autoplay').checked
        };

        // Check if Android platform and handle keystore
        const isAndroid = selectedPlatform === 'android' || selectedPlatform === 'android_aab';

        // Upload app icon if provided
        if (iconFile.files && iconFile.files.length > 0) {
            try {
                const iconFormData = new FormData();
                iconFormData.append('icon', iconFile.files[0]);

                const iconResponse = await fetch('/api/upload/icon', {
                    method: 'POST',
                    body: iconFormData
                });

                if (iconResponse.ok) {
                    const iconResult = await iconResponse.json();
                    formData.icon_path = iconResult.path;
                }
            } catch (error) {
                console.error('Icon upload error:', error);
            }
        }

        if (isAndroid && keystoreFile.files && keystoreFile.files.length > 0) {
            // Upload keystore first
            try {
                const keystoreFormData = new FormData();
                keystoreFormData.append('keystore', keystoreFile.files[0]);

                const uploadResponse = await fetch('/api/upload/keystore', {
                    method: 'POST',
                    body: keystoreFormData
                });

                if (uploadResponse.ok) {
                    const uploadResult = await uploadResponse.json();
                    formData.keystore_path = uploadResult.path;
                    formData.keystore_password = document.getElementById('keystore-password').value;
                    formData.key_alias = document.getElementById('key-alias').value;
                    formData.key_password = document.getElementById('key-password').value;
                }
            } catch (error) {
                console.error('Keystore upload error:', error);
            }
        }

        // Disable button and show progress
        buildButton.disabled = true;
        buildProgress.style.display = 'block';
        buildComplete.style.display = 'none';

        // Show center progress bar and hide dropdown
        platformDropdownWrapper.style.display = 'none';
        centerProgress.style.display = 'flex';

        try {
            // Start build
            const response = await fetch('/api/build', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Build failed to start');
            }

            const result = await response.json();
            const buildId = result.build_id;

            // Poll for status
            pollBuildStatus(buildId);

        } catch (error) {
            console.error('Build error:', error);
            showToast('Error starting build: ' + error.message, 'error');
            resetBuildUI();
        }
    });

    function resetBuildUI() {
        buildButton.disabled = false;
        buildProgress.style.display = 'none';
        centerProgress.style.display = 'none';
        platformDropdownWrapper.style.display = 'flex';
        centerProgressFill.style.width = '0%';
    }

    async function pollBuildStatus(buildId) {
        try {
            const response = await fetch(`/api/build/${buildId}/status`);

            if (!response.ok) {
                throw new Error('Failed to get build status');
            }

            const status = await response.json();

            // Update progress UI (both sidebar and center)
            progressFill.style.width = status.progress + '%';
            progressPercent.textContent = status.progress + '%';
            progressMessage.textContent = status.message;

            // Update center progress bar
            centerProgressFill.style.width = status.progress + '%';
            centerProgressText.textContent = status.message;

            if (status.status === 'completed') {
                // Show completion
                buildProgress.style.display = 'none';
                buildComplete.style.display = 'block';
                buildButton.disabled = false;

                // Hide center progress and show dropdown
                centerProgress.style.display = 'none';
                platformDropdownWrapper.style.display = 'flex';
                centerProgressFill.style.width = '0%';

                // Generate download links
                downloadLinks.innerHTML = '';
                if (status.outputs) {
                    for (const [platform, path] of Object.entries(status.outputs)) {
                        if (path.startsWith('Error:')) {
                            const errorBtn = document.createElement('span');
                            errorBtn.className = 'download-btn error';
                            errorBtn.innerHTML = `
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <circle cx="12" cy="12" r="10"/>
                                    <line x1="15" y1="9" x2="9" y2="15"/>
                                    <line x1="9" y1="9" x2="15" y2="15"/>
                                </svg>
                                ${getPlatformDisplayName(platform)} failed
                            `;
                            errorBtn.title = path;
                            downloadLinks.appendChild(errorBtn);
                        } else {
                            const link = document.createElement('a');
                            link.href = `/api/build/${buildId}/download/${platform}`;
                            link.className = 'download-btn';
                            link.innerHTML = `
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
                                    <polyline points="7 10 12 15 17 10"/>
                                    <line x1="12" y1="15" x2="12" y2="3"/>
                                </svg>
                                Download ${getPlatformDisplayName(platform)}
                            `;
                            downloadLinks.appendChild(link);
                        }
                    }

                    // Add keystore download link if generated
                    if (status.keystore_generated) {
                        const keystoreLink = document.createElement('a');
                        keystoreLink.href = `/api/build/${buildId}/download/keystore`;
                        keystoreLink.className = 'download-btn';
                        keystoreLink.innerHTML = `
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                                <path d="M7 11V7a5 5 0 0110 0v4"/>
                            </svg>
                            Download Keystore
                        `;
                        keystoreLink.title = 'Save this keystore for future app updates';
                        downloadLinks.appendChild(keystoreLink);
                    }
                }

                showToast('Build completed successfully!', 'success');
            } else if (status.status === 'error') {
                showToast('Build failed: ' + status.message, 'error');
                resetBuildUI();
            } else {
                // Continue polling
                setTimeout(() => pollBuildStatus(buildId), 1000);
            }
        } catch (error) {
            console.error('Status poll error:', error);
            showToast('Error checking build status: ' + error.message, 'error');
            resetBuildUI();
        }
    }

    function getPlatformDisplayName(platform) {
        const names = {
            'android': 'Android APK',
            'android_aab': 'Android AAB',
            'ios': 'iOS',
            'macos': 'macOS',
            'windows': 'Windows',
            'linux': 'Linux'
        };
        return names[platform] || platform;
    }

    // Toast notification function
    function showToast(message, type = 'info') {
        // Remove existing toasts
        const existingToast = document.querySelector('.toast');
        if (existingToast) {
            existingToast.remove();
        }

        const toast = document.createElement('div');
        toast.className = `toast ${type}`;

        const icon = type === 'success'
            ? '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 11-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>'
            : '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>';

        toast.innerHTML = `${icon}<span>${message}</span>`;
        document.body.appendChild(toast);

        // Remove toast after 4 seconds
        setTimeout(() => {
            toast.style.animation = 'slideIn 0.2s ease reverse';
            setTimeout(() => toast.remove(), 200);
        }, 4000);
    }

    // Auto-generate package name from app name
    const appNameInput = document.getElementById('app-name');
    const packageNameInput = document.getElementById('package-name');

    appNameInput.addEventListener('input', function() {
        if (!packageNameInput.dataset.userModified) {
            const sanitized = this.value.toLowerCase()
                .replace(/[^a-z0-9]/g, '')
                .substring(0, 20);
            packageNameInput.value = sanitized ? `com.example.${sanitized}` : '';
        }
    });

    packageNameInput.addEventListener('input', function() {
        this.dataset.userModified = 'true';
    });

    // Drag and drop for keystore
    const keystoreUpload = document.getElementById('keystore-upload');

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        keystoreUpload.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        keystoreUpload.addEventListener(eventName, () => {
            keystoreUploadLabel.style.borderColor = 'var(--primary)';
            keystoreUploadLabel.style.background = 'var(--primary-glow)';
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        keystoreUpload.addEventListener(eventName, () => {
            if (!keystoreFile.files || keystoreFile.files.length === 0) {
                keystoreUploadLabel.style.borderColor = '';
                keystoreUploadLabel.style.background = '';
            }
        }, false);
    });

    keystoreUpload.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;

        if (files.length > 0) {
            keystoreFile.files = files;
            const event = new Event('change');
            keystoreFile.dispatchEvent(event);
        }
    }, false);

    // Drag and drop for icon
    const iconUpload = document.getElementById('icon-upload');

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        iconUpload.addEventListener(eventName, preventDefaults, false);
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        iconUpload.addEventListener(eventName, () => {
            iconUploadLabel.style.borderColor = 'var(--primary)';
            iconUploadLabel.style.background = 'var(--primary-glow)';
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        iconUpload.addEventListener(eventName, () => {
            if (!iconFile.files || iconFile.files.length === 0) {
                iconUploadLabel.style.borderColor = '';
                iconUploadLabel.style.background = '';
            }
        }, false);
    });

    iconUpload.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;

        if (files.length > 0 && files[0].type.startsWith('image/')) {
            iconFile.files = files;
            const event = new Event('change');
            iconFile.dispatchEvent(event);
        }
    }, false);

    // ==================== Project Save/Open ====================

    // Save project button handler
    saveProjectBtn.addEventListener('click', async function() {
        const appName = document.getElementById('app-name').value;
        const appVersion = document.getElementById('app-version').value;
        const buildNumber = document.getElementById('build-number').value;

        // Validate required fields
        if (!appName) {
            showToast('Please enter an app name before saving', 'error');
            return;
        }
        if (!appVersion) {
            showToast('Please enter an app version before saving', 'error');
            return;
        }
        if (!buildNumber) {
            showToast('Please enter a build number before saving', 'error');
            return;
        }

        // Upload icon first if present and not already uploaded
        if (iconFile.files && iconFile.files.length > 0 && !currentIconPath) {
            try {
                const iconFormData = new FormData();
                iconFormData.append('icon', iconFile.files[0]);

                const iconResponse = await fetch('/api/upload/icon', {
                    method: 'POST',
                    body: iconFormData
                });

                if (iconResponse.ok) {
                    const iconResult = await iconResponse.json();
                    currentIconPath = iconResult.path;
                }
            } catch (error) {
                console.error('Icon upload error:', error);
            }
        }

        // Upload keystore if present and not already uploaded
        if (keystoreFile.files && keystoreFile.files.length > 0 && !currentKeystorePath) {
            try {
                const keystoreFormData = new FormData();
                keystoreFormData.append('keystore', keystoreFile.files[0]);

                const keystoreResponse = await fetch('/api/upload/keystore', {
                    method: 'POST',
                    body: keystoreFormData
                });

                if (keystoreResponse.ok) {
                    const keystoreResult = await keystoreResponse.json();
                    currentKeystorePath = keystoreResult.path;
                }
            } catch (error) {
                console.error('Keystore upload error:', error);
            }
        }

        // Collect project data
        const projectData = {
            app_name: appName,
            app_description: document.getElementById('app-description').value,
            app_version: appVersion,
            build_number: buildNumber,
            package_name: document.getElementById('package-name').value,
            web_url: document.getElementById('web-url').value,
            // WebView settings
            allow_zoom: document.getElementById('allow-zoom').checked,
            enable_javascript: document.getElementById('enable-javascript').checked,
            enable_dom_storage: document.getElementById('enable-dom-storage').checked,
            enable_geolocation: document.getElementById('enable-geolocation').checked,
            enable_pull_refresh: document.getElementById('enable-pull-refresh').checked,
            show_navigation: document.getElementById('show-navigation').checked,
            enable_file_access: document.getElementById('enable-file-access').checked,
            enable_cache: document.getElementById('enable-cache').checked,
            enable_media_autoplay: document.getElementById('enable-media-autoplay').checked,
            // Keystore info
            keystore_password: document.getElementById('keystore-password').value,
            key_alias: document.getElementById('key-alias').value,
            key_password: document.getElementById('key-password').value,
            // Asset paths
            icon_path: currentIconPath,
            keystore_path: currentKeystorePath
        };

        try {
            saveProjectBtn.disabled = true;
            saveProjectBtn.innerHTML = `
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin">
                    <circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-dashoffset="32"/>
                </svg>
                <span>Saving...</span>
            `;

            const response = await fetch('/api/project/save', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(projectData)
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Failed to save project');
            }

            // Download the file
            const blob = await response.blob();
            const safeName = appName.replace(/[^a-zA-Z0-9_-]/g, '_');
            const filename = `${safeName}_v${appVersion}_${buildNumber}.swab`;

            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            a.remove();

            showToast('Project saved successfully!', 'success');
        } catch (error) {
            console.error('Save error:', error);
            showToast('Error saving project: ' + error.message, 'error');
        } finally {
            saveProjectBtn.disabled = false;
            saveProjectBtn.innerHTML = `
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M19 21H5a2 2 0 01-2-2V5a2 2 0 012-2h11l5 5v11a2 2 0 01-2 2z"/>
                    <polyline points="17 21 17 13 7 13 7 21"/>
                    <polyline points="7 3 7 8 15 8"/>
                </svg>
                <span>Save</span>
            `;
        }
    });

    // Open project button handler
    openProjectBtn.addEventListener('click', function() {
        openProjectFile.click();
    });

    // Handle project file selection
    openProjectFile.addEventListener('change', async function() {
        if (!this.files || this.files.length === 0) return;

        const file = this.files[0];
        if (!file.name.endsWith('.swab')) {
            showToast('Please select a .swab project file', 'error');
            return;
        }

        const formData = new FormData();
        formData.append('project', file);

        try {
            openProjectBtn.disabled = true;
            openProjectBtn.innerHTML = `
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="spin">
                    <circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-dashoffset="32"/>
                </svg>
                <span>Opening...</span>
            `;

            const response = await fetch('/api/project/open', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || 'Failed to open project');
            }

            // Load project data into form
            const project = result.project;

            document.getElementById('app-name').value = project.app_name || '';
            document.getElementById('app-description').value = project.app_description || '';
            document.getElementById('app-version').value = project.app_version || '1.0.0';
            document.getElementById('build-number').value = project.build_number || '1';
            document.getElementById('package-name').value = project.package_name || '';
            document.getElementById('package-name').dataset.userModified = 'true';
            document.getElementById('web-url').value = project.web_url || '';

            // Update preview
            if (project.web_url) {
                updatePreview(project.web_url);
            }

            // WebView settings
            document.getElementById('allow-zoom').checked = project.allow_zoom !== false;
            document.getElementById('enable-javascript').checked = project.enable_javascript !== false;
            document.getElementById('enable-dom-storage').checked = project.enable_dom_storage !== false;
            document.getElementById('enable-geolocation').checked = project.enable_geolocation !== false;
            document.getElementById('enable-pull-refresh').checked = project.enable_pull_refresh !== false;
            document.getElementById('show-navigation').checked = project.show_navigation !== false;
            document.getElementById('enable-file-access').checked = project.enable_file_access !== false;
            document.getElementById('enable-cache').checked = project.enable_cache !== false;
            document.getElementById('enable-media-autoplay').checked = project.enable_media_autoplay === true;

            // Sync settings dialog checkboxes
            document.getElementById('setting-allow-zoom').checked = project.allow_zoom !== false;
            document.getElementById('setting-enable-javascript').checked = project.enable_javascript !== false;
            document.getElementById('setting-enable-dom-storage').checked = project.enable_dom_storage !== false;
            document.getElementById('setting-enable-geolocation').checked = project.enable_geolocation !== false;
            document.getElementById('setting-enable-pull-refresh').checked = project.enable_pull_refresh !== false;
            document.getElementById('setting-show-navigation').checked = project.show_navigation !== false;
            document.getElementById('setting-enable-file-access').checked = project.enable_file_access !== false;
            document.getElementById('setting-enable-cache').checked = project.enable_cache !== false;
            document.getElementById('setting-enable-media-autoplay').checked = project.enable_media_autoplay === true;

            // Keystore info
            if (project.keystore_password) {
                document.getElementById('keystore-password').value = project.keystore_password;
            }
            if (project.key_alias) {
                document.getElementById('key-alias').value = project.key_alias;
            }
            if (project.key_password) {
                document.getElementById('key-password').value = project.key_password;
            }

            // Handle icon
            if (project.icon_path) {
                currentIconPath = project.icon_path;
                // Show icon preview by loading from uploads
                iconPreview.innerHTML = `<img src="/uploads/${project.icon_path.split('/').pop()}" alt="App Icon" onerror="this.parentElement.innerHTML='<svg width=\\'48\\' height=\\'48\\' viewBox=\\'0 0 24 24\\' fill=\\'none\\' stroke=\\'currentColor\\' stroke-width=\\'1.5\\'><rect x=\\'3\\' y=\\'3\\' width=\\'18\\' height=\\'18\\' rx=\\'4\\' ry=\\'4\\'/><circle cx=\\'8.5\\' cy=\\'8.5\\' r=\\'1.5\\'/><polyline points=\\'21 15 16 10 5 21\\'/></svg>'">`;
                iconPreview.classList.add('has-icon');
                iconUploadLabel.innerHTML = `
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M22 11.08V12a10 10 0 11-5.93-9.14"/>
                        <polyline points="22 4 12 14.01 9 11.01"/>
                    </svg>
                    <span>Change Icon</span>
                `;
            }

            // Handle keystore
            if (project.keystore_path) {
                currentKeystorePath = project.keystore_path;
                keystoreUploadLabel.innerHTML = `
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M22 11.08V12a10 10 0 11-5.93-9.14"/>
                        <polyline points="22 4 12 14.01 9 11.01"/>
                    </svg>
                    <span>keystore.jks (loaded)</span>
                    <small class="hint">Click to change file</small>
                `;
                keystoreUploadLabel.style.borderColor = 'var(--success)';
                keystoreUploadLabel.style.background = 'var(--success-bg)';
                keystoreDetails.style.display = 'block';

                // Show keystore section if we have keystore data
                keystoreSection.style.display = 'block';
            }

            // Reset build UI
            buildProgress.style.display = 'none';
            buildComplete.style.display = 'none';

            showToast('Project loaded successfully!', 'success');
        } catch (error) {
            console.error('Open error:', error);
            showToast('Error opening project: ' + error.message, 'error');
        } finally {
            openProjectBtn.disabled = false;
            openProjectBtn.innerHTML = `
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M22 19a2 2 0 01-2 2H4a2 2 0 01-2-2V5a2 2 0 012-2h5l2 3h9a2 2 0 012 2z"/>
                </svg>
                <span>Open</span>
            `;
            // Reset file input
            openProjectFile.value = '';
        }
    });

    // Track icon upload path
    const originalIconChangeHandler = iconFile.onchange;
    iconFile.addEventListener('change', function() {
        // Reset the stored path when a new file is selected
        currentIconPath = null;
    });

    // Track keystore upload path
    keystoreFile.addEventListener('change', function() {
        // Reset the stored path when a new file is selected
        currentKeystorePath = null;
    });
});
