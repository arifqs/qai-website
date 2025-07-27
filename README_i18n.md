# QualityAI Website - Internationalization (i18n) Implementation

This document describes the internationalization (i18n) system implemented for the QualityAI website using web.py's built-in features with enhanced session management.

## Features

### ✅ Implemented Features

1. **Session-based Language Management**
   - Language preference stored in server-side sessions
   - Persistent across page navigation
   - 24-hour session timeout
   - Secure session handling with secret key

2. **Dual Language Support**
   - **English (en)**: Default language
   - **Japanese (jp)**: Secondary language

3. **Multiple Language Switching Methods**
   - URL parameters (backward compatibility): `/?lang=en` or `/?lang=jp`
   - Direct endpoint: `/set_language?lang=en&redirect=/current-page`
   - AJAX POST API: `POST /set_language` with `lang` parameter
   - Enhanced JavaScript interface with loading indicators

4. **Comprehensive Translation Coverage**
   - Navigation menus
   - Page content
   - Form labels and buttons
   - Footer information
   - Success/error messages

5. **Enhanced User Experience**
   - Visual language indicator in dropdown
   - Loading animation during language switch
   - Current language highlighting
   - Automatic page reload after language change
   - Fallback mechanisms for older browsers

## File Structure

```
├── app.py                          # Main application with i18n logic
├── locales/                        # Translation files
│   ├── en.json                     # English translations
│   └── jp.json                     # Japanese translations
├── template/
│   └── base.html                   # Base template with language switching UI
├── static/
│   └── language-switcher.js        # Enhanced JavaScript for language switching
├── sessions/                       # Session storage directory
├── test_i18n.py                   # Test script for i18n functionality
└── README_i18n.md                 # This documentation
```

## Technical Implementation

### 1. Session Management (`app.py`)

```python
# Session configuration
web.config.session_parameters['cookie_name'] = 'qai_session'
web.config.session_parameters['timeout'] = 86400  # 24 hours
web.config.session_parameters['secret_key'] = 'QualityAI_i18n_secret_key_2025'

# Session initialization
session = web.session.Session(app, web.session.DiskStore('sessions'), 
                             initializer={'language': 'en'})
```

### 2. Language Functions

- `get_user_language()`: Retrieve current language from session
- `set_user_language(lang_code)`: Set language preference in session
- `load_language(lang_code)`: Load translations from JSON file
- `setup_i18n()`: Initialize i18n for each request

### 3. URL Routing

```python
urls = (
    "/", "Index",
    "/set_language", "SetLanguage",  # New endpoint for language switching
    "/about_us", "About",
    "/product", "Product",
    "/services", "Services",
    '/static/(.*)', 'Static'
)
```

### 4. Language Switching Endpoint

The `/set_language` endpoint supports both GET and POST methods:

- **GET**: `http://example.com/set_language?lang=jp&redirect=/current-page`
- **POST**: JSON API for AJAX requests

### 5. Template Integration

Templates access translations via:
- `$messages['key']`: Translation text
- `$current_lang`: Current language code
- `<html lang="$current_lang">`: HTML language attribute

## Usage Examples

### 1. Basic Language Switching (Template)

```html
<a href="/set_language?lang=en&redirect=$web.ctx.path" class="language-switch" data-lang="en">
    English
</a>
<a href="/set_language?lang=jp&redirect=$web.ctx.path" class="language-switch" data-lang="jp">
    日本語
</a>
```

### 2. JavaScript API

```javascript
// Switch language programmatically
QAILanguageSwitcher.switchLanguage('jp', '/current-page');

// Get current language
const currentLang = QAILanguageSwitcher.getCurrentLanguage();

// Supported languages
console.log(QAILanguageSwitcher.SUPPORTED_LANGUAGES);
```

### 3. Python API (Server-side)

```python
# In your handler class
def GET(self):
    # Setup i18n (automatically handles session)
    current_lang, messages = setup_i18n()
    
    # Access current language
    print(f"Current language: {current_lang}")
    
    # Access translations
    print(f"Logo text: {messages['logo']}")
    
    return render.template_name()
```

## Translation File Format

Translation files are stored in JSON format in the `locales/` directory:

### `locales/en.json`
```json
{
  "logo": "Quality AI",
  "home": "Home",
  "product": "Product",
  "services": "Services",
  "about_us": "About Us",
  "langu": "Language"
}
```

### `locales/jp.json`
```json
{
  "logo": "クオリティ AI",
  "home": "ホーム",
  "product": "製品",
  "services": "サービス",
  "about_us": "私たちについて",
  "langu": "言語"
}
```

## Testing

### 1. Automated Testing

Run the test script to verify i18n functionality:

```bash
python test_i18n.py
```

The test script checks:
- Translation file validity
- Language switching functionality
- Session persistence
- API endpoints
- Cross-page language consistency

### 2. Manual Testing

1. **Start the server**:
   ```bash
   python app.py
   ```

2. **Test language switching**:
   - Click language dropdown in navigation
   - Select different languages
   - Navigate between pages
   - Verify language persistence

3. **Test backward compatibility**:
   - Use URL parameters: `http://localhost:8080/?lang=jp`
   - Verify redirect to clean URL with session

## Browser Compatibility

- **Modern Browsers**: Full AJAX functionality with loading indicators
- **Older Browsers**: Fallback to page redirect method
- **JavaScript Disabled**: Direct URL-based language switching still works

## Session Security

- Sessions stored server-side in `sessions/` directory
- Session cookies are HTTP-only by default
- Secret key used for session integrity
- 24-hour session timeout for security
- IP change tolerance for mobile users

## Performance Considerations

- Translation files cached in memory
- Minimal overhead per request
- Session data stored on disk (can be moved to Redis/Memcached)
- AJAX language switching reduces page reloads

## Extending the System

### Adding New Languages

1. Create translation file: `locales/[lang_code].json`
2. Add language to `SUPPORTED_LANGUAGES` in `app.py`
3. Add language option to template dropdown
4. Update JavaScript `SUPPORTED_LANGUAGES` object

### Adding New Translation Keys

1. Add key-value pairs to all language files
2. Use in templates: `$messages['new_key']`
3. Run test script to verify completeness

## Troubleshooting

### Common Issues

1. **Session not persisting**:
   - Check `sessions/` directory permissions
   - Verify session configuration
   - Clear browser cookies

2. **Language not switching**:
   - Check translation files are valid JSON
   - Verify language code in `SUPPORTED_LANGUAGES`
   - Check browser console for JavaScript errors

3. **Missing translations**:
   - Verify key exists in both language files
   - Check for typos in key names
   - Run test script to identify missing keys

### Debug Mode

Enable debug output in `app.py`:

```python
web.config.debug = True  # Add this line for debugging
```

## License

This i18n implementation is part of the QualityAI website project.

---

**Last Updated**: January 2025  
**Web.py Version**: Compatible with web.py 0.62+  
**Python Version**: 3.6+
