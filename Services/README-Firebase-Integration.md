# Firebase Integration for Service Pages

This document explains how to implement Firebase content loading for service pages in the Vardhman Associates website.

## Overview

The Firebase integration allows service pages to dynamically load content from the Firebase Firestore database, making it easy to update service content through the admin panel without modifying HTML files.

## Files Created

1. **`firebase-config.js`** - Firebase configuration and initialization
2. **`service-content-loader.js`** - Main functionality for fetching and displaying service content
3. **`auto-load-service.js`** - Simple script for automatic content loading
4. **`service-page-template.html`** - Template for creating new service pages

## How It Works

### 1. Automatic Content Detection

The system automatically detects:

- **Service Type**: From the URL path (CA, CS, or Advocate)
- **Service Title**: From the page title or filename

### 2. Content Loading Process

1. Page loads with a `#service-content` container
2. Shows loading spinner while fetching content
3. Fetches content from Firebase Firestore using service type and title
4. Displays the content or shows appropriate error/empty state messages

## Implementation Steps

### For New Service Pages

1. **Use the Template**: Copy `service-page-template.html` and customize it
2. **Add Content Container**: Ensure you have `<div id="service-content">` in the main content area
3. **Include the Script**: Add `<script type="module" src="../auto-load-service.js"></script>`
4. **Set Page Title**: Make sure the page title matches the service name in Firebase

### For Existing Service Pages

1. **Add Content Container**:

   ```html
   <div class="main-content">
     <div id="service-content">
       <!-- Content will be loaded from Firebase here -->
     </div>
   </div>
   ```

2. **Include the Script**:

   ```html
   <script type="module" src="../auto-load-service.js"></script>
   ```

3. **Ensure Page Title**: Make sure the page title matches the service name in Firebase

## Firebase Data Structure

The system expects data in the following structure in Firestore:

**Collection**: `services`
**Document Fields**:

- `type`: Service type (CA, CS, or Advocate)
- `title`: Service title (must match page title)
- `content`: HTML content for the service

### Example Document:

```json
{
  "type": "CA",
  "title": "Start A Business",
  "content": "<h2>Starting Your Business</h2><p>Content here...</p>"
}
```

## Error Handling

The system handles various scenarios:

1. **Content Not Found**: Shows "Content Coming Soon" message
2. **Network Error**: Shows error message with retry button
3. **Invalid Service**: Shows warning message
4. **Loading State**: Shows spinner while fetching content

## Styling

The system includes comprehensive CSS styling for:

- Headings (h1-h6)
- Paragraphs and lists
- Images and tables
- Loading states and error messages

## Admin Panel Integration

Content can be managed through the admin panel at `/admin/manage-services.html`:

1. Select service type (CA, CS, Advocate)
2. Choose service from dropdown
3. Click "Edit Content" to open rich text editor
4. Save content to Firebase

## Troubleshooting

### Common Issues:

1. **Content Not Loading**:

   - Check if service type and title match Firebase data
   - Verify Firebase configuration
   - Check browser console for errors

2. **Page Title Mismatch**:

   - Ensure page title exactly matches service title in Firebase
   - Check for extra spaces or special characters

3. **Firebase Connection Issues**:
   - Verify Firebase configuration
   - Check network connectivity
   - Ensure Firebase project is active

### Debug Mode:

Add this to browser console to debug:

```javascript
// Check detected service type and title
console.log("Service Type:", getServiceTypeFromPath());
console.log("Service Title:", getServiceTitleFromPage());
```

## Security Considerations

- Firebase configuration is public (required for client-side access)
- Firestore security rules should be configured to allow read access to services collection
- Admin panel should have proper authentication

## Performance

- Content is cached by browser
- Loading states provide good user experience
- Error handling prevents page crashes
- Responsive design works on all devices
