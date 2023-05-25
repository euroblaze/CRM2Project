function onChangeCheckbox(ev) {
    let dataKey = ev.getAttribute('data-key');
    let note = document.querySelector(`textarea[data-key='${dataKey}']`);
    if (ev.checked) note.removeAttribute('disabled');
    else note.setAttribute('disabled', true);
}