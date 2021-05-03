import React, { useEffect, useState } from 'react';
import classNames from 'classnames';
import { useSelector } from 'react-redux';
import { currentDivAtom } from '../../services/state';
import { useAtom } from 'jotai';

function NavElement(props) {
    return (
        <li>
            <a id={'nav-' + props.navId + '-' + props.pos} onClick={(e) => props.click(e)}
                className={classNames(
                    {active: props.isActive}
                )}>
                {props.navName}{props.activeFiles ? ' ('+ props.activeFiles +')': ''}
            </a>
        </li>
    )
}

function Navbar() {
    const [items, setItems] = useState([true]);
    const [currentDiv,setCurrent] = useAtom(currentDivAtom);
    const files = useSelector(state => state.items.items);

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
        setCurrent(getId);
    }
    let tabNames = [
        {id: 'preview', name: 'Antesala'}, {id: 'uploading', name: 'Por subir'},
        {id: 'completed', name: 'Subidos'}, {id: 'error', name: 'Errores'}];

    return (
        <ul className="navbar-tabs group">
            {tabNames.map((el, index) => (
                <NavElement pos={index} key={index} navId={el.id} click={handleNavClick}
                    navName={el.name} isActive={items[index]} activeFiles={files.filter(item => item.status.value == el.id).length} />
            ))}
        </ul>
    )
}

export default Navbar;