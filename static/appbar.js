function go() {
    if(firstname && lastname) {
        let profileLink = document.querySelector('.profile_link_tag');
        profileLink.setAttribute('href', '/music/profile/');
        profileLink.text = firstname + ' ' + lastname;
    }
}

window.onload = go();