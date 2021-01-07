import React, { useState } from 'react';
import classNames from 'classnames';

function NavElement({ pos, navId, navName, isActive, click}) {
    return (
        <li>
            <a id={'nav-' + navId + '-' + pos} onClick={(e) => click(e)}
                className={classNames(
                    {active: isActive}
                )}>
                {navName}
            </a>
        </li>
    )
}

function Navbar() {
    const [items, setItems] = useState([true]);

    const handleNavClick = (e) => {
        let getId = e.target.id.split('-')[1]
        let getPos = e.target.id.split('-')[2]
        let contentDivs = document.getElementsByClassName('statusDiv')
        let toSetItems = [];
        for(let i=0;i<contentDivs.length;i++){
            contentDivs[i].style.display = 'none';
            if (i != getPos) 
                toSetItems.push(false)
            else
                toSetItems.push(true)
        }
        document.getElementById(getId).style.display = 'block';
        setItems(toSetItems)
    }
    let tabNames = [
        {id: 'preview', name: 'Antesala'}, {id: 'uploading', name: 'Por subir'},
        {id: 'completed', name: 'Subidos'}, {id: 'error', name: 'Errores'}];
    return (
        <ul className="navbar-tabs group">
            {tabNames.map((el, index) => (
                <NavElement pos={index} key={index} navId={el.id} click={handleNavClick}
                    navName={el.name} isActive={items[index]} />
            ))}
        </ul>
    )
}

export default Navbar;