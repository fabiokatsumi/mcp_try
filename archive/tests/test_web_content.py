#!/usr/bin/env python3
"""
Test the web interface content to verify emoji encoding
"""

import requests

def test_web_content():
    """Test the web interface content"""
    try:
        # Get the web page content
        response = requests.get("http://192.168.254.95:8080", 
                              headers={'Cache-Control': 'no-cache'})
        
        print("Response Status:", response.status_code)
        print("Content-Type:", response.headers.get('content-type'))
        print("Content Encoding:", response.encoding)
        
        # Check for emoji in content
        content = response.text
        
        print("\n=== Checking for emojis ===")
        if "🚀" in content:
            print("✅ Found rocket emoji: 🚀")
        else:
            print("❌ Rocket emoji not found")
            
        if "ðŸš€" in content:
            print("❌ Found broken emoji encoding: ðŸš€")
        else:
            print("✅ No broken emoji encoding found")
            
        # Find the title section
        if "<h1>" in content:
            start = content.find("<h1>")
            end = content.find("</h1>", start)
            if start != -1 and end != -1:
                title = content[start:end+5]
                print(f"\nTitle section: {title}")
        
        print("\n=== First 500 characters ===")
        print(repr(content[:500]))
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_web_content()
