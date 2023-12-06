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