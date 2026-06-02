document.addEventListener('DOMContentLoaded', function () {
    // Create the UI elements
    const container = document.createElement('div');
    container.className = 'text-helper';

    const inputContainer = document.createElement('div');
    inputContainer.className = 'url-input-container';

    const urlInput = document.createElement('input');
    urlInput.type = 'url';
    urlInput.placeholder = 'Enter URL to fetch content';
    urlInput.className = 'url-input';

    const fetchButton = document.createElement('button');
    fetchButton.textContent = 'Fetch Content';
    fetchButton.className = 'fetch-button';

    const contentContainer = document.createElement('div');
    contentContainer.className = 'content-container';
    contentContainer.style.marginTop = '20px';
    contentContainer.style.display = 'none';

    // Add elements to the page
    inputContainer.appendChild(urlInput);
    inputContainer.appendChild(fetchButton);
    container.appendChild(inputContainer);
    container.appendChild(contentContainer);

    // Insert after the title or at the beginning of the content
    const existingContent = document.querySelector('.post-content') || document.querySelector('article') || document.body;
    if (existingContent.firstChild) {
        existingContent.insertBefore(container, existingContent.firstChild);
    } else {
        existingContent.appendChild(container);
    }

    // Handle fetch button click
    fetchButton.addEventListener('click', function () {
        const url = urlInput.value.trim();
        if (!url) {
            alert('Please enter a URL');
            return;
        }

        // Show loading state
        contentContainer.style.display = 'block';
        contentContainer.innerHTML = '<p>Loading content...</p>';

        // Call the API to fetch the URL content
        fetch(`https://lzwjava.shop/text?url=${encodeURIComponent(url)}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                // Display the content
                contentContainer.innerHTML = `
                    <h3>Fetched Content:</h3>
                    <div class="fetched-content">${data.content || data.text || JSON.stringify(data)}</div>
                `;
            })
            .catch(error => {
                contentContainer.innerHTML = `<p>Error fetching content: ${error.message}</p>`;
                console.error('Error:', error);
            });
    });

    // Allow Enter key to trigger fetch
    urlInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            fetchButton.click();
        }
    });
});
