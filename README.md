# Google Play Developer API MCP Server

A Model Context Protocol (MCP) server for managing Google Play app deployment and in-app products via the Android Publisher API v3.

## Features

### App Deployment
- **deploy_internal**: Upload AAB and deploy to internal testing track

### In-App Products
- **create_inapp_product**: Create or update a single in-app product
- **batch_create_inapp_products**: Create multiple products at once
- **activate_inapp_product**: Activate a draft product
- **batch_activate_inapp_products**: Activate multiple products
- **deactivate_inapp_product**: Deactivate an active product
- **list_inapp_products**: List all one-time products
- **list_subscriptions**: List all subscription products

### App Info
- **get_app_info**: Get app track and version information

## Requirements

- Python 3.10+
- Google Cloud service account with Google Play Developer API access
- App registered in Google Play Console

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/google-play-mcp.git
cd google-play-mcp
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```bash
cp .env.example .env
# Edit .env with your settings
```

## Configuration

### Service Account Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Google Play Android Developer API**
4. Go to **IAM & Admin** → **Service Accounts**
5. Create a new service account
6. Create and download a JSON key file
7. Go to [Google Play Console](https://play.google.com/console)
8. Navigate to **Settings** → **API access**
9. Link your Google Cloud project
10. Grant access to the service account with appropriate permissions

### Environment Variables

Create a `.env` file in the project root:

```
GOOGLE_PLAY_KEY_FILE=/path/to/your-service-account-key.json
GOOGLE_PLAY_PACKAGE_NAME=com.yourcompany.yourapp
```

## Usage with Claude Code

Add to your `.mcp.json` configuration:

```json
{
  "mcpServers": {
    "google-play": {
      "command": "/path/to/google-play-mcp/.venv/bin/python",
      "args": ["/path/to/google-play-mcp/server.py"]
    }
  }
}
```

## Tool Examples

### Deploy to Internal Testing

```
Deploy app-release.aab to internal testing with Korean and English release notes
```

### Create In-App Product

```
Create an in-app product:
- SKU: gems_100
- Korean: 보석 100개 / 보석 100개를 획득합니다
- English: 100 Gems / Get 100 gems
- Price: $0.99 USD
```

### Batch Create Products

```json
[
  {"sku": "gems_12", "title_ko": "보석 12개", "title_en": "12 Gems",
   "description_ko": "보석 12개 획득", "description_en": "Get 12 gems", "price_usd": 0.99},
  {"sku": "gems_66", "title_ko": "보석 66개", "title_en": "66 Gems",
   "description_ko": "보석 66개 획득", "description_en": "Get 66 gems", "price_usd": 4.99}
]
```

### Activate Products

```json
["gems_12", "gems_66", "gems_136"]
```

## Important Notes

### Prerequisites for In-App Products

Before creating in-app products, your app must have:

1. `com.android.vending.BILLING` permission in `AndroidManifest.xml`
2. Play Billing Library 6.0.1+ (Flutter: `in_app_purchase` package)
3. A bundle with these uploaded to Google Play

### Draft Apps

Apps that have never been published can only use `status: "draft"` for deployments.
You must manually publish through Google Play Console for the first release.

### API Migration

This server uses the new `monetization.onetimeproducts` API instead of the deprecated
`inappproducts` API which returns 403 errors.

### Price Conversion

USD prices are automatically converted to 170+ regional currencies using
Google's `convertRegionPrices` API.

## Tracks

| Track | Description |
|-------|-------------|
| `internal` | Internal testing (up to 100 testers) |
| `alpha` | Closed testing |
| `beta` | Open testing |
| `production` | Production release |

## License

MIT License
