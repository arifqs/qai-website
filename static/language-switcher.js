/**
 * QualityAI Language Switcher
 * Enhanced internationalization (i18n) functionality with session management
 */

(function() {
    'use strict';

    // Language configuration
    const SUPPORTED_LANGUAGES = {
        'en': 'English',
        'jp': '日本語'
    };

    // Initialize language switcher when DOM is loaded
    document.addEventListener('DOMContentLoaded', function() {
        console.log('Language switcher initialized');
        initLanguageSwitcher();
        highlightCurrentLanguage();
    });

    /**
     * Initialize language switcher functionality
     */
    function initLanguageSwitcher() {
        const languageLinks = document.querySelectorAll('.language-switch');
        console.log('Found language links:', languageLinks.length);
        
        languageLinks.forEach(function(link) {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                const lang = this.getAttribute('data-lang');
                const currentPath = window.location.pathname;
                
                console.log('Language link clicked:', lang, 'current path:', currentPath);
                
                // Switch language using direct redirect (no loading indicator needed)
                switchLanguage(lang, currentPath);
            });
        });
    }

    /**
     * Switch language using direct redirect (more reliable)
     */
    function switchLanguage(lang, redirectPath) {
        console.log('Switching language to:', lang);
        
        // Use direct GET request for more reliable language switching
        const url = '/set_language?lang=' + encodeURIComponent(lang) + 
                   '&redirect=' + encodeURIComponent(redirectPath || '/');
        console.log('Redirecting to:', url);
        
        // Direct redirect is more reliable than AJAX for session-based language switching
        window.location.href = url;
    }

    /**
     * Highlight current language in the dropdown
     */
    function highlightCurrentLanguage() {
        // Get current language from body data attribute or other indicator
        const currentLang = getCurrentLanguage();
        console.log('Current language detected:', currentLang);
        
        if (currentLang) {
            const languageLinks = document.querySelectorAll('.language-switch');
            languageLinks.forEach(function(link) {
                const linkLang = link.getAttribute('data-lang');
                if (linkLang === currentLang) {
                    link.style.fontWeight = 'bold';
                    link.style.color = '#007bff';
                    
                    // Add current language indicator
                    if (!link.querySelector('.current-lang-indicator')) {
                        const indicator = document.createElement('span');
                        indicator.className = 'current-lang-indicator';
                        indicator.innerHTML = ' ✓';
                        indicator.style.color = '#28a745';
                        link.appendChild(indicator);
                    }
                }
            });
        }
    }

    /**
     * Get current language from various sources
     */
    function getCurrentLanguage() {
        // Try to get from HTML lang attribute
        const htmlLang = document.documentElement.lang;
        if (htmlLang && SUPPORTED_LANGUAGES[htmlLang]) {
            return htmlLang;
        }

        // Try to get from body data attribute
        const bodyLang = document.body.getAttribute('data-lang');
        if (bodyLang && SUPPORTED_LANGUAGES[bodyLang]) {
            return bodyLang;
        }

        // Try to detect from content (as last resort)
        return detectLanguageFromContent();
    }

    /**
     * Detect language from page content
     */
    function detectLanguageFromContent() {
        const title = document.title;
        const logoText = document.querySelector('.sitename');
        
        // Simple detection based on Japanese characters
        const hasJapanese = /[ひらがなカタカナー一-龯]/.test(
            title + (logoText ? logoText.textContent : '')
        );
        
        return hasJapanese ? 'jp' : 'en';
    }


    /**
     * Add CSS for language switcher styling
     */
    const style = document.createElement('style');
    style.textContent = `
        .language-switch.current {
            font-weight: bold !important;
            color: #007bff !important;
        }
        .current-lang-indicator {
            color: #28a745 !important;
        }
    `;
    document.head.appendChild(style);

    // Export for potential external use
    window.QAILanguageSwitcher = {
        switchLanguage: switchLanguage,
        getCurrentLanguage: getCurrentLanguage,
        SUPPORTED_LANGUAGES: SUPPORTED_LANGUAGES
    };

})();
