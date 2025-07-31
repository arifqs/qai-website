#!/usr/bin/env python3
"""
Test script for QualityAI i18n functionality
"""

import requests
import json
import time

def test_language_switching():
    """Test the language switching functionality"""
    base_url = "http://localhost:8080"
    
    print("Testing QualityAI i18n functionality...")
    print("=" * 50)
    
    # Test 1: Default language (English)
    print("Test 1: Default language")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✓ Default page loads successfully")
            # Check for English content
            if "Quality AI" in response.text:
                print("✓ English content detected")
            else:
                print("✗ English content not found")
        else:
            print(f"✗ Failed to load default page: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("✗ Server not running. Please start the server first.")
        return False
    
    # Test 2: Switch to Japanese
    print("\nTest 2: Switch to Japanese")
    try:
        # Use session to maintain cookies
        session = requests.Session()
        
        # Switch to Japanese
        response = session.get(f"{base_url}/set_language?lang=jp")
        if response.status_code == 200 or response.status_code == 302:
            print("✓ Language switch to Japanese successful")
            
            # Check Japanese page
            response = session.get(f"{base_url}/")
            if "クオリティ AI" in response.text:
                print("✓ Japanese content detected")
            else:
                print("✗ Japanese content not found")
        else:
            print(f"✗ Failed to switch to Japanese: {response.status_code}")
    except Exception as e:
        print(f"✗ Error testing Japanese switch: {e}")
    
    # Test 3: Switch back to English
    print("\nTest 3: Switch back to English")
    try:
        response = session.get(f"{base_url}/set_language?lang=en")
        if response.status_code == 200 or response.status_code == 302:
            print("✓ Language switch to English successful")
            
            # Check English page
            response = session.get(f"{base_url}/")
            if "Quality AI" in response.text and "クオリティ AI" not in response.text:
                print("✓ English content restored")
            else:
                print("✗ English content not properly restored")
        else:
            print(f"✗ Failed to switch back to English: {response.status_code}")
    except Exception as e:
        print(f"✗ Error testing English switch: {e}")
    
    # Test 4: Test POST API
    print("\nTest 4: Test POST API for language switching")
    try:
        response = session.post(f"{base_url}/set_language", data={"lang": "jp"})
        if response.status_code == 200:
            result = json.loads(response.text)
            if result.get('success'):
                print("✓ POST API language switch successful")
                print(f"  Current language: {result.get('language')}")
            else:
                print(f"✗ POST API failed: {result.get('message')}")
        else:
            print(f"✗ POST API request failed: {response.status_code}")
    except Exception as e:
        print(f"✗ Error testing POST API: {e}")
    
    # Test 5: Test different pages
    print("\nTest 5: Test language persistence across pages")
    pages = ["/about_us", "/product", "/services"]
    
    for page in pages:
        try:
            response = session.get(f"{base_url}{page}")
            if response.status_code == 200:
                if "クオリティ AI" in response.text:
                    print(f"✓ Japanese content on {page}")
                else:
                    print(f"✗ Japanese content not found on {page}")
            else:
                print(f"✗ Failed to load {page}: {response.status_code}")
        except Exception as e:
            print(f"✗ Error testing {page}: {e}")
    
    print("\n" + "=" * 50)
    print("Test completed!")
    return True

def test_translation_files():
    """Test that translation files are properly formatted"""
    print("\nTesting translation files...")
    print("-" * 30)
    
    languages = ["en", "jp"]
    for lang in languages:
        try:
            with open(f"locales/{lang}.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                print(f"✓ {lang}.json is valid JSON with {len(data)} keys")
                
                # Check for required keys
                required_keys = ["logo", "home", "product", "services", "about_us", "langu"]
                missing_keys = [key for key in required_keys if key not in data]
                
                if missing_keys:
                    print(f"✗ Missing keys in {lang}.json: {missing_keys}")
                else:
                    print(f"✓ All required keys present in {lang}.json")
                    
        except FileNotFoundError:
            print(f"✗ Translation file {lang}.json not found")
        except json.JSONDecodeError as e:
            print(f"✗ Invalid JSON in {lang}.json: {e}")
        except Exception as e:
            print(f"✗ Error reading {lang}.json: {e}")

if __name__ == "__main__":
    print("QualityAI i18n Test Suite")
    print("========================")
    
    # Test translation files first
    test_translation_files()
    
    # Test web functionality
    print("\nStarting web functionality tests...")
    print("Make sure the server is running with: python app.py")
    input("Press Enter to continue when server is ready...")
    
    test_language_switching()
