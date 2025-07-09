# MCP Server LAN Access Guide 🌐

Your MCP server is now configured and running with full LAN accessibility and **enterprise security options**! This guide explains how to access and use your MCP server from any device on your network.

## 🚀 Current Status

✅ **Server Running**: Your MCP server is active and accessible  
✅ **HTTP Wrapper**: Provides REST API access over HTTP  
✅ **LAN Access**: Available to all devices on your local network  
✅ **Web Interface**: User-friendly web UI with proper emoji support  
✅ **Dynamic Tools**: Tools automatically refresh in web UI every 30 seconds  
✅ **CORS Enabled**: Cross-origin requests supported  
✅ **UTF-8 Encoding**: Proper emoji and international character support  
🔒 **NEW: Security Features**: Enterprise-grade authentication and monitoring available

## 📍 Access Points

### 🔓 Development Servers (No Authentication)
| Server Type | Local URL | LAN URL | Use Case |
|-------------|-----------|---------|----------|
| **HTTP Server** | `http://localhost:8080` | `http://192.168.254.95:8080` | Development/Testing |
| **Cloud Server** | `http://localhost:8080` | `http://192.168.254.95:8080` | Cloud Demo |

### 🔒 Secure Server (API Key Required) - RECOMMENDED FOR PRODUCTION
| Server Type | Local URL | LAN URL | Use Case |
|-------------|-----------|---------|----------|
| **Secure Server** | `http://localhost:8443` | `http://192.168.254.95:8443` | Production/Enterprise |

### 📡 API Endpoints

#### Development Endpoints (No Auth)
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Web interface |
| `/mcp` | POST | MCP protocol requests |
| `/api/tools` | GET | Dynamic tools discovery |

#### Secure Endpoints (Requires API Key)
| Endpoint | Method | Purpose | Auth Required |
|----------|--------|---------|---------------|
| `/health` | GET | Health check | ❌ No |
| `/` | GET | Secure web interface | ❌ No |
| `/mcp` | POST | MCP protocol requests | ✅ API Key |
| `/api/tools` | GET | Dynamic tools discovery | ✅ API Key |
| `/api/status` | GET | Server status & metrics | ✅ API Key |

## 🛠️ Available Tools

Your MCP server provides these tools (dynamically updated):

1. **⏰ `get_time`** - Get current date and time
2. **📖 `read_file`** - Read contents of any file
3. **✏️ `write_file`** - Write content to files
4. **📁 `list_directory`** - List directory contents
5. **🧮 `calculate`** - Perform basic mathematical calculations
6. **💻 `system_info`** - Get detailed system information

> **Note**: Tools are automatically discovered and displayed in the web UI. Any new tools you add will appear within 30 seconds or on page refresh.

## 💻 Quick Testing

### 🔓 Development Server Testing (No Authentication)
```bash
# Test server initialization
curl -X POST http://192.168.254.95:8080/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0", 
    "id": "1", 
    "method": "initialize",
    "params": {
      "protocolVersion": "2024-11-05",
      "capabilities": {},
      "clientInfo": {"name": "test-client", "version": "1.0.0"}
    }
  }'

# List available tools
curl -X POST http://192.168.254.95:8080/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "id": "2", "method": "tools/list"}'

# Get current time
curl -X POST http://192.168.254.95:8080/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0", 
    "id": "3", 
    "method": "tools/call",
    "params": {"name": "get_time", "arguments": {}}
  }'

# Calculate mathematical expression
curl -X POST http://192.168.254.95:8080/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0", 
    "id": "4", 
    "method": "tools/call",
    "params": {"name": "calculate", "arguments": {"expression": "2 + 3 * 4"}}
  }'

# Get system information
curl -X POST http://192.168.254.95:8080/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0", 
    "id": "5", 
    "method": "tools/call",
    "params": {"name": "system_info", "arguments": {}}
  }'

# Get dynamic tools list
curl -X GET http://192.168.254.95:8080/api/tools
```

### From PowerShell
```powershell
# Test with Invoke-RestMethod
$body = @{
    jsonrpc = "2.0"
    id = "1"
    method = "tools/list"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://192.168.254.95:8080/mcp" -Method POST -Body $body -ContentType "application/json"

# Get dynamic tools list
Invoke-RestMethod -Uri "http://192.168.254.95:8080/api/tools" -Method GET

# Test calculator tool
$calcBody = @{
    jsonrpc = "2.0"
    id = "calc1"
    method = "tools/call"
    params = @{
        name = "calculate"
        arguments = @{
            expression = "10 * (5 + 3)"
        }
    }
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://192.168.254.95:8080/mcp" -Method POST -Body $calcBody -ContentType "application/json"
```

### From Python
```python
import requests

# Test the server tools list
response = requests.post(
    "http://192.168.254.95:8080/mcp",
    json={
        "jsonrpc": "2.0",
        "id": "1", 
        "method": "tools/list"
    }
)
print(response.json())

# Get dynamic tools
tools_response = requests.get("http://192.168.254.95:8080/api/tools")
print(tools_response.json())

# Test calculator
calc_response = requests.post(
    "http://192.168.254.95:8080/mcp",
    json={
        "jsonrpc": "2.0",
        "id": "calc1",
        "method": "tools/call",
        "params": {
            "name": "calculate",
            "arguments": {"expression": "2**8 + 15"}
        }
    }
)
print(calc_response.json())
```

### 🔒 Secure Server Testing (API Key Required)

First, generate an API key:
```bash
python secure_server.py --generate-key
```

Then start the secure server:
```bash
python secure_server.py --api-key YOUR_GENERATED_KEY
```

Test with authentication:
```bash
# Test health check (no auth required)
curl http://192.168.254.95:8443/health

# Test with API key authentication
curl -X POST http://192.168.254.95:8443/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "jsonrpc": "2.0", 
    "id": "1", 
    "method": "initialize",
    "params": {
      "protocolVersion": "2024-11-05",
      "capabilities": {},
      "clientInfo": {"name": "secure-test", "version": "1.0.0"}
    }
  }'

# Secure calculator call
curl -X POST http://192.168.254.95:8443/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "jsonrpc": "2.0", 
    "id": "4", 
    "method": "tools/call",
    "params": {"name": "calculate", "arguments": {"expression": "2**8 + 15 * 3"}}
  }'

# Get server status (requires auth)
curl -H "Authorization: Bearer YOUR_API_KEY" \
  http://192.168.254.95:8443/api/status
```

## 🌍 LAN Device Access

### From Other Computers
1. **Windows/Mac/Linux**: Open browser to `http://192.168.254.95:8080`
2. **Mobile devices**: Same URL works on phones/tablets
3. **Development tools**: Use the API endpoint in your applications

### From Different Programming Languages

#### JavaScript (Browser/Node.js)
```javascript
// Test tools list
fetch('http://192.168.254.95:8080/mcp', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        jsonrpc: "2.0",
        id: "1",
        method: "tools/list"
    })
})
.then(response => response.json())
.then(data => console.log(data));

// Get dynamic tools
fetch('http://192.168.254.95:8080/api/tools')
.then(response => response.json())
.then(data => console.log('Available tools:', data.tools));

// Test calculator
fetch('http://192.168.254.95:8080/mcp', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        jsonrpc: "2.0",
        id: "calc1",
        method: "tools/call",
        params: {
            name: "calculate",
            arguments: {expression: "Math.sqrt(144) + 10"}
        }
    })
})
.then(response => response.json())
.then(data => console.log('Calculation result:', data));
```

#### C# (.NET)
```csharp
using System.Text;
using System.Text.Json;

var client = new HttpClient();
var request = new {
    jsonrpc = "2.0",
    id = "1",
    method = "tools/list"
};

var json = JsonSerializer.Serialize(request);
var content = new StringContent(json, Encoding.UTF8, "application/json");
var response = await client.PostAsync("http://192.168.254.95:8080/mcp", content);
var result = await response.Content.ReadAsStringAsync();
```

## 🔧 Server Management

### Starting the Server
```powershell
cd "g:\Trading\Fabio\LLM_try\mcp_try"
python http_server.py
```

### Stopping the Server
- Press `Ctrl+C` in the terminal where the server is running
- Or close the terminal window

### Checking Server Status
- Visit `http://192.168.254.95:8080` in your browser (beautiful web UI with dynamic tools)
- Or run the test client: `python test_lan_client.py`
- Or test dynamic tools: `python test_dynamic_tools.py`
- Or use the server manager: `python server_manager.py status`

## 🛡️ Security Considerations

Since your server is accessible on the LAN:

1. **File Access**: The server can read/write files in its directory
2. **Network Access**: Any device on your network can use the server
3. **No Authentication**: Currently no password protection (suitable for trusted networks)

### Recommended Security Practices
- Only run on trusted networks
- Monitor server logs for unusual activity
- Consider adding authentication for production use
- Limit file access to specific directories if needed

## 🚨 Troubleshooting

### Common Issues

1. **Server not accessible**
   - Check if Windows Firewall is blocking port 8080
   - Verify the server is running with `python http_server.py`

2. **Connection refused**
   - Ensure you're using the correct IP address (192.168.254.95)
   - Try `http://localhost:8080` if accessing from the same machine

3. **Emoji display issues**
   - Server now properly supports UTF-8 encoding
   - If you see broken emojis (ðŸš€), force refresh with `Ctrl+Shift+R`
   - Or open browser developer tools and disable cache

4. **Tools not updating**
   - Tools refresh automatically every 30 seconds in web UI
   - For immediate update, refresh the page manually
   - Check `/api/tools` endpoint for current tools list

### Firewall Configuration (if needed)
```powershell
# Allow incoming connections on port 8080 (run as Administrator)
New-NetFirewallRule -DisplayName "MCP Server" -Direction Inbound -Port 8080 -Protocol TCP -Action Allow
```

## 📱 Mobile Access

Your MCP server works great on mobile devices:

1. **iPhone/iPad**: Open Safari and go to `http://192.168.254.95:8080`
2. **Android**: Open Chrome and use the same URL
3. **Mobile Apps**: Use the API endpoint in mobile app development

## 🔗 Integration Examples

### With Excel/VBA
```vba
Sub TestMCPServer()
    Dim xhr As Object
    Set xhr = CreateObject("MSXML2.XMLHTTP")
    
    xhr.Open "POST", "http://192.168.254.95:8080/mcp", False
    xhr.setRequestHeader "Content-Type", "application/json"
    
    Dim jsonData As String
    jsonData = "{""jsonrpc"":""2.0"",""id"":""1"",""method"":""tools/list""}"
    
    xhr.send jsonData
    MsgBox xhr.responseText
End Sub
```

### With R
```r
library(httr)
library(jsonlite)

response <- POST(
  "http://192.168.254.95:8080/mcp",
  body = list(
    jsonrpc = "2.0",
    id = "1",
    method = "tools/list"
  ),
  encode = "json"
)

content(response, "text")
```

## 📈 Usage Statistics

Your server logs all requests. Check the terminal output to see:
- Request timestamps
- Client IP addresses  
- Method calls
- Response status

## 🎯 Next Steps

1. **Test from other devices**: Try accessing from phones, tablets, other computers
2. **Build applications**: Use the API in your own projects
3. **Add more tools**: Extend the MCP server with additional functionality (they'll auto-appear in web UI!)
4. **Monitor usage**: Watch the server logs to see how it's being used
5. **Try the new tools**: Test the calculator and system info tools
6. **Explore dynamic features**: Watch tools update automatically in the web interface

## 🆕 Recent Updates

- ✅ **Dynamic Tool Discovery**: Tools now auto-refresh in web UI
- ✅ **UTF-8 Support**: Proper emoji display (🚀 ✅ 📡 🔧 ⏰ 📖 ✏️ 📁 🧮 💻)
- ✅ **New Tools Added**: Calculator and system info tools
- ✅ **API Endpoints**: `/api/tools` for dynamic tool discovery
- ✅ **Auto-Refresh**: Web UI updates every 30 seconds
- ✅ **Enhanced Web Interface**: Modern design with gradient background

---

**Your MCP server is now fully operational and accessible across your LAN! 🎉**

For support or questions, check the README.md file or the test scripts in the project directory.
