/**
 * Gmail-style document preview modal.
 *
 * Any element with class "js-doc-view" and a "data-file-url" attribute
 * will open the file in a popup on the same page, with a Download button,
 * just like clicking an attachment preview in Gmail.
 *
 *   <a class="js-doc-view" data-file-url="{{ project.document_file.url }}"
 *      data-file-name="{{ project.title }}">View</a>
 *
 * .docx files are rendered client-side with mammoth.js.
 * .pdf files are shown natively in an iframe.
 * Any other file type falls back to a "download to view" message.
 */
(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        var overlay = document.getElementById('docviewerOverlay');
        if (!overlay) return;

        var closeBtn = document.getElementById('docviewerCloseBtn');
        var downloadBtn = document.getElementById('docviewerDownloadBtn');
        var fileNameEl = document.getElementById('docviewerFileName');
        var loadingEl = document.getElementById('docviewerLoading');
        var docxEl = document.getElementById('docviewerDocxContent');
        var frameEl = document.getElementById('docviewerFrame');
        var unsupportedEl = document.getElementById('docviewerUnsupported');

        function resetPanes() {
            loadingEl.style.display = 'flex';
            docxEl.style.display = 'none';
            docxEl.innerHTML = '';
            frameEl.style.display = 'none';
            frameEl.src = 'about:blank';
            unsupportedEl.style.display = 'none';
        }

        function getExtension(url) {
            var clean = url.split('?')[0].split('#')[0];
            var parts = clean.split('.');
            return parts.length > 1 ? parts.pop().toLowerCase() : '';
        }

        function openViewer(fileUrl, fileName) {
            resetPanes();

            if (!fileUrl) {
                fileNameEl.textContent = fileName || 'Document';
                downloadBtn.style.display = 'none';
                overlay.classList.add('is-open');
                document.body.style.overflow = 'hidden';
                showUnsupported('No file has been uploaded yet.');
                return;
            }

            downloadBtn.style.display = '';
            fileNameEl.textContent = fileName || 'Document';
            downloadBtn.setAttribute('href', fileUrl);
            downloadBtn.setAttribute('download', fileName || '');
            overlay.classList.add('is-open');
            document.body.style.overflow = 'hidden';

            var ext = getExtension(fileUrl);

            // Confirm the file actually exists before handing it to an <iframe>,
            // otherwise a missing file just shows the browser's own broken-page
            // icon inside the frame with no explanation.
            fetch(fileUrl, { method: 'HEAD' })
                .then(function (res) {
                    if (!res.ok) throw new Error('not found');
                    renderFile(ext, fileUrl);
                })
                .catch(function () {
                    showUnsupported("This file couldn't be found. It may not have been uploaded yet, or the link is out of date.");
                });
        }

        function renderFile(ext, fileUrl) {
            if (ext === 'pdf') {
                frameEl.onload = function () {
                    loadingEl.style.display = 'none';
                    frameEl.style.display = 'block';
                };
                frameEl.onerror = function () {
                    showUnsupported("This file couldn't be loaded. Please use the Download button above.");
                };
                frameEl.src = fileUrl;
                return;
            }

            if (ext === 'docx') {
                if (typeof mammoth === 'undefined') {
                    showUnsupported();
                    return;
                }
                fetch(fileUrl)
                    .then(function (res) {
                        if (!res.ok) throw new Error('Could not fetch file');
                        return res.arrayBuffer();
                    })
                    .then(function (buffer) {
                        return mammoth.convertToHtml({ arrayBuffer: buffer });
                    })
                    .then(function (result) {
                        docxEl.innerHTML = result.value || '<p><em>This document appears to be empty.</em></p>';
                        docxEl.style.display = 'block';
                        loadingEl.style.display = 'none';
                    })
                    .catch(function () {
                        showUnsupported();
                    });
                return;
            }

            // .doc (legacy binary), .ppt, .xls, images handled by browser via iframe, etc.
            if (['png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'].indexOf(ext) !== -1) {
                docxEl.innerHTML = '<div style="text-align:center;"><img src="' + fileUrl + '" style="max-width:100%;border-radius:6px;"></div>';
                docxEl.style.display = 'block';
                loadingEl.style.display = 'none';
                return;
            }

            if (ext === 'txt') {
                fetch(fileUrl)
                    .then(function (res) { return res.text(); })
                    .then(function (text) {
                        docxEl.innerHTML = '<pre style="white-space:pre-wrap;font-family:inherit;">' + escapeHtml(text) + '</pre>';
                        docxEl.style.display = 'block';
                        loadingEl.style.display = 'none';
                    })
                    .catch(showUnsupported);
                return;
            }

            showUnsupported();
        }

        function showUnsupported(message) {
            loadingEl.style.display = 'none';
            unsupportedEl.querySelector('p').innerHTML = message ||
                "A live preview isn't available for this file type.<br>Please use the Download button above to view it.";
            unsupportedEl.style.display = 'flex';
        }

        function escapeHtml(str) {
            var div = document.createElement('div');
            div.appendChild(document.createTextNode(str));
            return div.innerHTML;
        }

        function closeViewer() {
            overlay.classList.remove('is-open');
            document.body.style.overflow = '';
            frameEl.src = 'about:blank';
        }

        document.addEventListener('click', function (e) {
            var trigger = e.target.closest('.js-doc-view');
            if (trigger) {
                e.preventDefault();
                var url = trigger.getAttribute('data-file-url');
                var name = trigger.getAttribute('data-file-name');
                openViewer(url, name);
            }
        });

        closeBtn.addEventListener('click', closeViewer);
        overlay.addEventListener('click', function (e) {
            if (e.target === overlay) closeViewer();
        });
        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && overlay.classList.contains('is-open')) closeViewer();
        });
    });
})();
