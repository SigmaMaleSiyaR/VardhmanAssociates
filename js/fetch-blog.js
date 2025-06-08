// Initialize Firebase
const firebaseConfig = {
    apiKey: "AIzaSyAV6RSeZ1j5krYodWKIXGNJE1sY_l9pvh8",
    authDomain: "vardhamanassociates-861f9.firebaseapp.com",
    projectId: "vardhamanassociates-861f9",
    storageBucket: "vardhamanassociates-861f9.appspot.com",
    messagingSenderId: "322122751719",
    appId: "1:322122751719:web:9f4ae6936a8bf144244c42",
    measurementId: "G-Y06T3Q22YD"
};

// Initialize Firebase
if (!firebase.apps.length) {
    firebase.initializeApp(firebaseConfig);
}
const db = firebase.firestore();

// Function to create blog card
function createBlogCard(id, blog) {
    console.log('Creating card for blog:', blog);
    
    // Handle date formatting
    let formattedDate = 'No date';
    if (blog.createdAt) {
        try {
            // Check if it's a Firestore Timestamp
            if (blog.createdAt.toDate) {
                formattedDate = new Date(blog.createdAt.toDate()).toLocaleDateString();
            } else if (blog.createdAt instanceof Date) {
                formattedDate = blog.createdAt.toLocaleDateString();
            } else if (typeof blog.createdAt === 'string') {
                formattedDate = new Date(blog.createdAt).toLocaleDateString();
            } else if (typeof blog.createdAt === 'number') {
                formattedDate = new Date(blog.createdAt).toLocaleDateString();
            }
        } catch (error) {
            console.error('Error formatting date:', error);
        }
    }

    // Truncate description to 100 characters
    const truncatedDescription = blog.description 
        ? (blog.description.length > 100 
            ? blog.description.substring(0, 100) + '...' 
            : blog.description)
        : 'No description available';

    return `
        <div class="col" style="min-width: 300px; max-width: 350px; padding: 0 0.5rem;">
            <div class="card h-100 shadow-sm" style="border-radius: 8px; transition: all 0.3s ease; cursor: pointer;" 
                 onmouseover="this.style.transform='translateY(-5px)'; this.style.boxShadow='0 4px 15px rgba(0,0,0,0.1)';" 
                 onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 4px rgba(0,0,0,0.05)';">
                <div style="height: 150px; overflow: hidden; border-radius: 8px 8px 0 0;">
                    <img src="${blog.imageUrl || 'https://via.placeholder.com/300x150'}" 
                         class="card-img-top" 
                         alt="${blog.title}" 
                         style="height: 100%; width: 100%; object-fit: cover;">
                </div>
                <div class="card-body" style="padding: 1rem;">
                    <h5 class="card-title text-truncate mb-2" style="font-size: 1.1rem; font-weight: 600;" title="${blog.title || 'Untitled'}">
                        ${blog.title || 'Untitled'}
                    </h5>
                    <p class="card-text" style="font-size: 0.9rem; line-height: 1.4; height: 2.8em; overflow: hidden; color: #666;">
                        ${truncatedDescription}
                    </p>
                </div>
                <div class="card-footer bg-white border-top-0 py-2" style="padding: 0.5rem 1rem;">
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted">
                            <i class="far fa-calendar-alt me-1"></i>
                            ${formattedDate}
                        </small>
                        <small class="text-muted">
                            <i class="far fa-eye me-1"></i>
                            <span class="view-count">0</span> views
                        </small>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Function to load view count
async function loadViewCount(blogId, element) {
    try {
        const viewDoc = await db.collection("blog_views").doc(blogId).get();
        if (viewDoc && viewDoc.data()) {
            const data = viewDoc.data();
            element.textContent = data.count || 0;
        }
    } catch (error) {
        console.error("Error loading view count:", error);
        element.textContent = '0';
    }
}

// Function to load blogs
async function loadBlogs(limit = null) {
    const container = document.getElementById('blogContainer');
    const spinner = document.getElementById('loadingSpinner');
    
    try {
        spinner.classList.remove('d-none');
        container.innerHTML = '';

        console.log('Fetching blogs...');
        let blogsQuery = db.collection("blogs").orderBy("createdAt", "desc");
        
        // If limit is specified, only fetch that many blogs
        if (limit) {
            blogsQuery = blogsQuery.limit(limit);
        }
        
        const querySnapshot = await blogsQuery.get();
        console.log('Blogs fetched:', querySnapshot.size);
        
        if (querySnapshot.empty) {
            console.log('No blogs found in the database');
            container.innerHTML = '<div class="col-12 text-center"><p class="text-muted">No blogs found.</p></div>';
            return;
        }

        querySnapshot.forEach((doc) => {
            const blog = doc.data();
            console.log('Processing blog:', blog.title);
            const cardHtml = createBlogCard(doc.id, blog);
            container.innerHTML += cardHtml;
            
            // Load view count for the last added card
            const lastCard = container.lastElementChild;
            const viewCountElement = lastCard.querySelector('.view-count');
            loadViewCount(doc.id, viewCountElement);

            // Add click event to navigate to blog
            lastCard.addEventListener('click', () => {
                // Store the blog ID in localStorage
                localStorage.setItem('currentBlogId', doc.id);
                // Open blog in new tab
                window.open('blog.html', '_blank');
            });
        });
    } catch (error) {
        console.error("Error loading blogs:", error);
        container.innerHTML = '<div class="col-12 text-center"><p class="text-danger">Error loading blogs. Please try again later.</p></div>';
    } finally {
        spinner.classList.add('d-none');
    }
}

// Load blogs when the page loads
document.addEventListener('DOMContentLoaded', () => {
    console.log('Page loaded, initializing Firebase...');
    loadBlogs();
}); 