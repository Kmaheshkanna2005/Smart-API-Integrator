import os

def generate_wrapper(api_metadata, language="python"):
    base_url = api_metadata.get("base_url", "").rstrip("/")
    endpoint = api_metadata.get("endpoint", "")
    if not endpoint.startswith("/"):
        endpoint = "/" + endpoint
        
    method = api_metadata.get("method", "GET").upper()
    auth_type = api_metadata.get("auth_type", "None")
    header_name = api_metadata.get("auth_header_name", "Authorization")
    body_template = api_metadata.get("body_template", {})

    if language.lower() == "javascript":
        # --- JAVASCRIPT TEMPLATE ---
        code = f"""
/**
 * Auto-generated API Client (JavaScript)
 */
class ApiClient {{
    constructor(apiKey = null) {{
        this.baseUrl = "{base_url}";
        this.apiKey = apiKey;
        this.headers = {{ "Content-Type": "application/json" }};
        
        if (this.apiKey) {{
            if ("{auth_type}" === "Bearer") {{
                this.headers["{header_name}"] = `Bearer ${{this.apiKey}}`;
            }} else {{
                this.headers["{header_name}"] = this.apiKey;
            }}
        }}
    }}

    async callApi(data = null, userId = null) {{
        let currentEndpoint = "{endpoint}";
        if (userId) {{
            if (currentEndpoint.includes("{{user_id}}")) {{
                currentEndpoint = currentEndpoint.replace("{{user_id}}", userId);
            }} else {{
                currentEndpoint = `${{currentEndpoint.replace(/\\/+$/, "")}}/${{userId}}`;
            }}
        }}

        const url = `${{this.baseUrl}}${{currentEndpoint}}`;
        console.log(`\\n--- Making {method} request to: ${{url}} ---`);

        try {{
            const response = await fetch(url, {{
                method: "{method}",
                headers: this.headers,
                body: {method} !== "GET" ? JSON.stringify(data) : null
            }});

            if (!response.ok) throw new Error(`HTTP error! status: ${{response.status}}`);

            const contentType = response.headers.get("content-type");
            if (contentType && contentType.includes("application/json")) {{
                return await response.json();
            }} else {{
                return {{ text_response: await response.text() }};
            }}
        }} catch (error) {{
            return {{ error: error.message }};
        }}
    }}
}}

// Example usage
(async () => {{
    const client = new ApiClient();
    const result = await client.callApi({body_template if method != "GET" else "null"}, { "1" if "{{user_id}}" in endpoint else "null" });
    console.log("Response:", result);
}})();
"""
        filename = "generated_api_client.js"
    else:
        # --- PYTHON TEMPLATE (Your existing logic) ---
        code = f"""import requests
import json

class ApiClient:
    def __init__(self, api_key=None):
        self.base_url = "{base_url}"
        self.api_key = api_key
        self.headers = {{}}
        if self.api_key:
            self.headers["{header_name}"] = f"Bearer {{self.api_key}}" if "{auth_type}" == "Bearer" else self.api_key

    def call_api(self, data=None, user_id=None):
        current_endpoint = "{endpoint}"
        if user_id:
            if "{{user_id}}" in current_endpoint:
                current_endpoint = current_endpoint.replace("{{user_id}}", str(user_id))
            else:
                current_endpoint = f"{{current_endpoint.rstrip('/')}}/{{user_id}}"
        
        url = f"{{self.base_url}}{{current_endpoint}}"
        print(f"\\n--- Making {method} request to: {{url}} ---")
        try:
            response = requests.request("{method}", url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json() if 'application/json' in response.headers.get('Content-Type', '') else {{"text_response": response.text}}
        except Exception as e:
            return {{"error": str(e)}}

if __name__ == "__main__":
    client = ApiClient()
    result = client.call_api()
    print(json.dumps(result, indent=4))
"""
        filename = "generated_api_client.py"

    with open(filename, "w") as f:
        f.write(code)
    return filename