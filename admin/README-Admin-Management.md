# Admin Management System

This document explains how to use the admin management system for Vardhaman Associates.

## Overview

The admin management system allows super admins to:

- Add new admin accounts
- View all admin accounts
- Delete admin accounts
- Manage different admin roles

## Admin Roles

### Super Admin

- Can manage all content (blogs, services)
- Can add, view, and delete other admin accounts
- First user to log in automatically becomes a super admin
- Has access to the "Manage Admins" page

### Admin

- Can manage content (blogs, services)
- Cannot manage other admin accounts
- Cannot access the "Manage Admins" page

## Getting Started

### First Time Setup

1. **First Login**: The first user to log in to the admin panel will automatically become a super admin
2. **Access Admin Management**: Go to `/admin/manage-admins.html`
3. **Add More Admins**: Use the "Add New Admin" button to create additional admin accounts

### Adding New Admins

1. Navigate to `/admin/manage-admins.html`
2. Click "Add New Admin" button
3. Fill in the form:
   - **Email**: The login email for the new admin
   - **Password**: Minimum 6 characters
   - **Display Name**: Name to show in the admin panel
   - **Role**: Choose between "Admin" or "Super Admin"
4. Click "Add Admin"

### Managing Existing Admins

1. **View All Admins**: The admin list shows all current admin accounts
2. **Delete Admin**: Click the trash icon next to any admin (except yourself)
3. **Role Information**: See which admins are super admins vs regular admins

## Security Features

### Authentication

- All admin pages require authentication
- Only users in the `admins` collection can access admin features
- Automatic redirect to login page if not authenticated

### Authorization

- Only super admins can access the admin management page
- Regular admins are redirected away from admin management
- Users cannot delete their own accounts

### Data Structure

The admin data is stored in Firebase Firestore in the `admins` collection:

```javascript
{
  uid: "firebase-auth-uid",
  email: "admin@example.com",
  name: "Admin Name",
  role: "admin" | "super_admin",
  createdAt: timestamp
}
```

## Firebase Configuration

The system uses Firebase Authentication and Firestore:

- **Authentication**: For user login/logout
- **Firestore**: For storing admin records and content

## Navigation

All admin pages now include navigation to:

- Manage Blogs
- Manage Services
- Manage Admins (super admins only)

## Troubleshooting

### Common Issues

1. **"Access Denied" Error**

   - Only super admins can access admin management
   - Check if you're logged in as a super admin

2. **Can't Delete Admin**

   - You cannot delete your own account
   - Make sure you're a super admin

3. **New Admin Can't Login**
   - Check if the admin was properly added to the `admins` collection
   - Verify the email and password are correct

### Error Messages

- **"Only super admins can manage admin accounts"**: You need super admin privileges
- **"Error creating admin account"**: Check Firebase configuration and network connection
- **"Error deleting admin account"**: Check Firebase permissions and network connection

## Best Practices

1. **Create Super Admin First**: Always create a super admin account first
2. **Use Strong Passwords**: Require strong passwords for all admin accounts
3. **Regular Review**: Periodically review and clean up unused admin accounts
4. **Backup**: Keep a backup of important admin information
5. **Monitor Access**: Regularly check the admin list for unauthorized accounts

## Technical Notes

### Firebase Rules

Make sure your Firestore security rules allow admin operations:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /admins/{adminId} {
      allow read, write: if request.auth != null &&
        exists(/databases/$(database)/documents/admins/$(request.auth.uid)) &&
        get(/databases/$(database)/documents/admins/$(request.auth.uid)).data.role == 'super_admin';
    }
  }
}
```

### Browser Compatibility

- Modern browsers with ES6+ support
- Requires JavaScript enabled
- Works best with Chrome, Firefox, Safari, Edge

## Support

For technical support or questions about the admin management system, contact your system administrator.
