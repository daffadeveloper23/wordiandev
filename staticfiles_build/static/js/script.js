// Pop up forms
const openModalButtons = document.querySelectorAll('[data-modal-target]')
const closeModalButtons = document.querySelectorAll('[data-close-button]')
const overlay = document.getElementById('overlay')

openModalButtons.forEach(button => {
    button.addEventListener('click', () => {
        const modal = document.querySelector(button.dataset.modalTarget)
        openModal(modal)
    })
})

closeModalButtons.forEach(button => {
    button.addEventListener('click', () => {
        const modal = button.closest('.modal')
        closeModal(modal)
    })
})

function openModal(modal) {
    if (modal == null) return
    modal.classList.add('active')
    overlay.classList.add('active')
}

function closeModal(modal) {
    if (modal == null) return
    modal.classList.remove('active')
    overlay.classList.remove('active')
}

overlay.addEventListener('click', () => {
    const modals = document.querySelectorAll('.modal.active')
    modals.forEach(modal => {
        closeModal(modal)
    })
})

// Show and hide password
const showBtn1 = document.querySelector('.show1')
const showBtn2 = document.querySelector('.show2')
const showBtn3 = document.querySelector('.show3')
const showButtons = [showBtn1, showBtn2, showBtn3]

showButtons.forEach(button => {
    button.addEventListener('click', () => {
        if (button.textContent === 'Show Password') {
            if (button.classList.contains('show1')) {
                const req = 'password'
                showPassword(req)
            } else if (button.classList.contains('show2')) {
                const req = 'password2'
                showPassword(req)
            } else if (button.classList.contains('show3')) {
                const req = 'signin-password'
                showPassword(req)
            }
            button.textContent = 'Hide Password'
        } else {
            if (button.classList.contains('show1')) {
                const req = 'password'
                hidePassword(req)
            } else if (button.classList.contains('show2')) {
                const req = 'password2'
                hidePassword(req)
            } else if (button.classList.contains('show3')) {
                const req = 'signin-password'
                hidePassword(req)
            }
            button.textContent = 'Show Password'
        }
    })
})

function showPassword(req) {
    const elem = document.getElementById(req)
    elem.setAttribute('type', 'text')
}

function hidePassword(req) {
    const elem = document.getElementById(req)
    elem.setAttribute('type', 'password')
}


