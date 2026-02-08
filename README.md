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

## Installation & Usage

You can use this MCP server directly with `npx` without installing it manually.

### Quick Start (npx)

```bash
# Configure your API key
npx google-play-mcp init-key

# For Korean instructions (한국어 안내)
npx google-play-mcp init-key --lang ko

# Start the server
npx google-play-mcp start
```

### Installation (Global)

If you prefer to install it globally (from npm):

```bash
npm install -g google-play-mcp
```

### Installation (Local Dev)

To install from the cloned repository:

```bash
npm install -g .
```

Then you can run:

```bash
google-play-mcp init-key
google-play-mcp start
```

## Configuration (Antigravity & Claude Desktop)

To use this MCP server, add the following configuration to your MCP client (e.g., `claude_desktop_config.json` or Antigravity settings):

```json
{
  "mcpServers": {
    "google-play": {
      "command": "google-play-mcp",
      "args": ["start"],
      "env": {
        "GOOGLE_PLAY_KEY_FILE": "/absolute/path/to/your-key.json",
        "GOOGLE_PLAY_PACKAGE_NAME": "com.yourcompany.yourapp"
      }
    }
  }
}
```

> **Note:** If you haven't run `init-key` or don't have a `.env` file, you can pass environment variables directly in the configuration as shown above. If you have a `.env` file in the working directory, the server will load it automatically.

1. Login to npm:

```bash
npm login
```

1. Publish the package:

```bash
npm publish
```

## Configuration

The `npm run init-key` script will automatically create a `.env` file with your configuration:

```
GOOGLE_PLAY_KEY_FILE=/absolute/path/to/your-key.json
GOOGLE_PLAY_PACKAGE_NAME=com.yourcompany.yourapp
```

## Usage

To start the server manually:

```bash
npm start
```

### Usage with Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "google-play": {
      "command": "npm",
      "args": ["start"],
      "cwd": "/absolute/path/to/google-play-mcp"
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
