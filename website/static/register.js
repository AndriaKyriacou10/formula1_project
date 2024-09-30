document.addEventListener('DOMContentLoaded', () => {
    let driverSelect = document.querySelector('.r-select-driver');
    let constructorSelect = document.querySelector('.r-select-constructor');
    // let btn = document.querySelector('.btn-register');
    // let isScrolling = false;
    
    driverSelect.addEventListener('focus', () => {
        console.log('clicked');
        // driverSelect.style.marginTop = '40px';
        driverSelect.style.marginBottom = '500px';
        // btn.classList.add('btn-register-focus');
    });

    driverSelect.addEventListener('change', () => {
        console.log('changed')
        driverSelect.style.marginTop = '0px';
        driverSelect.style.marginBottom = '0px';
        driverSelect.blur();
        // btn.classList.remove('btn-register-focus');
    });
    driverSelect.addEventListener('blur', () => {
        console.log('blur')
        driverSelect.style.marginTop = '0px';
        driverSelect.style.marginBottom = '0px';
        // btn.classList.remove('btn-register-focus');
    });

    constructorSelect.addEventListener('change', () => {
        constructorSelect.blur()
    })

    // window.addEventListener('scroll', () => {
    //     console.log('scrolling')
    //     isScrolling = true;
    //     if (document.activeElement === driverSelect) {
    //         driverSelect.blur();
    //     }
    //     setTimeout(() => {
    //         console.log('not scrolling')
    //         isScrolling = false;
    //     }, 100);
    // });
});