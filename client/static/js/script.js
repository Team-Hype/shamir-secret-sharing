// Tab functionality
function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    
    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    
    tablinks = document.getElementsByClassName("tab");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

// Copy to clipboard functionality
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        alert('Copied to clipboard!');
    }, function(err) {
        console.error('Could not copy text: ', err);
    });
}

// Initialize the page
document.addEventListener('DOMContentLoaded', function() {
    // Add copy buttons to share boxes
    const shareBoxes = document.querySelectorAll('.share-box');
    shareBoxes.forEach(box => {
        const copyBtn = document.createElement('button');
        copyBtn.className = 'copy-btn';
        copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
        copyBtn.onclick = function() {
            copyToClipboard(box.textContent.trim());
        };
        box.appendChild(copyBtn);
    });
    
    // Custom file input handling
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        // Create container
        const container = document.createElement('div');
        container.className = 'file-input-container';
        
        // Create label
        const label = document.createElement('label');
        label.className = 'file-input-label';
        label.innerHTML = '<i class="fas fa-cloud-upload-alt"></i> Choose a file';
        label.htmlFor = input.id;
        
        // Create file name span
        const fileNameSpan = document.createElement('span');
        fileNameSpan.className = 'file-name';
        label.appendChild(fileNameSpan);
        
        // Replace original input with our custom implementation
        input.parentNode.insertBefore(container, input);
        container.appendChild(input);
        container.appendChild(label);
        
        // Update filename when a file is selected
        input.addEventListener('change', function() {
            if (input.files.length > 0) {
                fileNameSpan.textContent = input.files[0].name;
            } else {
                fileNameSpan.textContent = '';
            }
        });
    });
}); 