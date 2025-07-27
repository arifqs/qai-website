import web
import model
import os
import json
from web import template
from cheroot.server import HTTPServer
from cheroot.ssl.builtin import BuiltinSSLAdapter

HTTPServer.ssl_adapter = BuiltinSSLAdapter(
        certificate='ssl/fullchain.pem',
        private_key='ssl/privkey.pem')

urls = (
    "/", "Index",
    '/static/(.*)', 'Static',
    "/career", "Career",
    "/product", "Product",
    "/services", "Services",
    "/set_language", "SetLanguage"
)

# Language configuration
SUPPORTED_LANGUAGES = ['en', 'jp']
DEFAULT_LANGUAGE = 'en'

# Create the application
app = web.application(urls, globals())

render = template.render("template", base="base")
template.Template.globals['ctx'] = web.ctx
template.Template.globals['web'] = web

def get_user_language():
    """Get user's preferred language from cookie or default"""
    try:
        # Get language from cookie
        cookies = web.cookies()
        lang = cookies.get('qai_lang', DEFAULT_LANGUAGE)
        print(f"Getting user language from cookie: {lang}")
        return lang
    except Exception as e:
        print(f"Error getting language: {e}")
        return DEFAULT_LANGUAGE

def set_user_language(lang_code):
    """Set user's preferred language in cookie"""
    if lang_code in SUPPORTED_LANGUAGES:
        try:
            print(f"Setting language cookie to: {lang_code}")
            # Set cookie for 30 days
            web.setcookie('qai_lang', lang_code, expires=86400*30)
            print(f"Language cookie set successfully")
            return True
        except Exception as e:
            print(f"Error setting language cookie: {e}")
            return False
    else:
        print(f"Invalid language code: {lang_code}")
        return False

def load_language(lang_code=None):
    """Load language translations from JSON file"""
    if lang_code is None:
        lang_code = get_user_language()
    
    if lang_code not in SUPPORTED_LANGUAGES:
        lang_code = DEFAULT_LANGUAGE
    
    path = os.path.join("locales", f"{lang_code}.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading language file {path}: {e}")
        # Fallback to default language
        if lang_code != DEFAULT_LANGUAGE:
            return load_language(DEFAULT_LANGUAGE)
        return {}

def setup_i18n():
    """Setup internationalization for current request"""
    # Get language from cookie
    current_lang = get_user_language()
    
    # Set language in web.config for backward compatibility
    web.config.lang = current_lang
    
    # Load messages and make them available to templates
    messages = load_language(current_lang)
    template.Template.globals['messages'] = messages
    template.Template.globals['current_lang'] = current_lang
    
    print(f"i18n setup - current_lang: {current_lang}")
    
    return current_lang, messages

class Index:
    def GET(self):
        # Check if language is being set via URL parameter (for backward compatibility)
        i = web.input()
        if 'lang' in i and i.lang in SUPPORTED_LANGUAGES:
            if set_user_language(i.lang):
                # Redirect to clean URL without lang parameter
                raise web.seeother('/')
        
        # Setup i18n
        current_lang, messages = setup_i18n()
        
        # Get data from model
        data = model.get_all_data_as_dict()
        print(f"Index page - Current language: {current_lang}")
        print("Loaded IDs:", list(data.keys()))
        
        return render.index(data)

    def POST(self):
        try:
            # Setup i18n for POST request
            current_lang, messages = setup_i18n()
            
            form = web.input()
            print(f"Contact form submitted: {form.name}")
            model.insert_contact(form.name, form.email, form.subject, form.message)
            
            # Return success message in current language
            if current_lang == 'en':
                return "Message Sent Successfully"
            elif current_lang == 'jp':
                return "メッセージは正常に送信されました"
            else:
                return "Message Sent Successfully"
        except Exception as e:
            return f"Error: {str(e)}"

class Static:
    def GET(self, path):
        return web.staticfile(path, root='static')

class About:
    def GET(self):
        # Check if language is being set via URL parameter
        i = web.input()
        if 'lang' in i and i.lang in SUPPORTED_LANGUAGES:
            if set_user_language(i.lang):
                raise web.seeother('/about_us')
        
        # Setup i18n
        setup_i18n()
        return render.about_us()

class Product:
    def GET(self):
        # Check if language is being set via URL parameter
        i = web.input()
        if 'lang' in i and i.lang in SUPPORTED_LANGUAGES:
            if set_user_language(i.lang):
                raise web.seeother('/product')
        
        # Setup i18n
        setup_i18n()
        return render.product()

class Career:
    def GET(self):
        # Check if language is being set via URL parameter
        i = web.input()
        if 'lang' in i and i.lang in SUPPORTED_LANGUAGES:
            if set_user_language(i.lang):
                raise web.seeother('/career')
        
        # Setup i18n
        setup_i18n()
        return render.career()

class Services:
    def GET(self):
        # Check if language is being set via URL parameter
        i = web.input()
        if 'lang' in i and i.lang in SUPPORTED_LANGUAGES:
            if set_user_language(i.lang):
                raise web.seeother('/services')
        
        # Setup i18n
        setup_i18n()
        return render.services()

class SetLanguage:
    def GET(self):
        """Handle language switching via GET request"""
        i = web.input()
        lang = i.get('lang', DEFAULT_LANGUAGE)
        redirect_url = i.get('redirect', '/')
        
        print(f"SetLanguage GET - lang: {lang}, redirect: {redirect_url}")
        
        if set_user_language(lang):
            print(f"Language successfully set to: {lang}")
            
            if redirect_url and redirect_url != '/':
                raise web.seeother(redirect_url)
            else:
                raise web.seeother('/')
        else:
            print(f"Failed to set language to: {lang}")
            # Invalid language, redirect to home
            raise web.seeother('/')
    
    def POST(self):
        """Handle language switching via POST request"""
        i = web.input()
        lang = i.get('lang', DEFAULT_LANGUAGE)
        
        print(f"SetLanguage POST - lang: {lang}")
        
        success = set_user_language(lang)
        current_lang = get_user_language()
        
        print(f"POST result - success: {success}, current_lang: {current_lang}")
        
        web.header('Content-Type', 'application/json')
        return json.dumps({
            'success': success,
            'language': current_lang,
            'message': 'Language updated' if success else 'Invalid language'
        })

if __name__ == '__main__':
    app.run()
