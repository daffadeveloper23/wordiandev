// document.addEventListener("DOMContentLoaded", () => {
//     alert("Work")
// })

// Pop up profile bar
const profileButton = document.querySelector('.profile-menu')
const profileBar = document.querySelector('.profile-bar')


profileButton.addEventListener('click', (event) => {
    event.stopPropagation()
    profileBar.classList.toggle('active')
})

document.addEventListener('click', (event) => {
    const targetElement = event.target

    if (
        !profileBar.contains(targetElement) &&
        !profileButton.contains(targetElement)
    ) {
        profileBar.classList.remove('active')
    }
})

// Textarea growth
function autoResize(textarea) {
    textarea.style.height = 'auto';  // Reset the height to auto to calculate the scrollHeight.
    textarea.style.height = textarea.scrollHeight + 'px';  // Set the height to match the content.
}

// Image upload
let imageInput = document.getElementById('image-upload')
let imagePreview = document.getElementById('image-preview')
let imageFrame = document.querySelector('.uploadedimg-frame')

imageInput.addEventListener('change', () => { // Show chosen image
    const file = imageInput.files[0]

    if (file) {
        const reader = new FileReader()

        reader.onload = (e) => {
            imageFrame.style.display = 'block'
            imagePreview.src = e.target.result
        }

        reader.readAsDataURL(file)
    } else {
        imagePreview.src = '#'
        imageFrame.style.display = 'none'
    }
})

// Form buttons trigger
const articleForm = document.getElementById('article-form')
const saveDraftButton = document.getElementById('save-draft')
const publishArticleButton = document.getElementById('publish-article')

saveDraftButton.addEventListener('click', () => {
    
    articleForm.setAttribute("action", "/update-draft")
    articleForm.submit()
})

publishArticleButton.addEventListener('click', () => {
    articleForm.setAttribute("action", "/publish-draft")
    articleForm.submit()
})