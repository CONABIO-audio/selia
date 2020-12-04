import React from 'react';
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

class Navbar extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            0: true
        }

        this.handleNavClick = this
        .handleNavClick
        .bind(this);
    }


    handleNavClick = (e) => {
        let getId = e.target.id.split('-')[1]
        let getPos = e.target.id.split('-')[2]
        let contentDivs = document.getElementsByClassName('statusDiv')
        for(let i=0;i<contentDivs.length;i++){
            contentDivs[i].style.display = 'none';
            this.setState({ [i]: false })
        }
        document.getElementById(getId).style.display = 'block';
        this.setState({ [getPos]: true })
    }
    render() {
        let tabNames = [
            {id: 'preview', name: 'Antesala'}, {id: 'uploading', name: 'Por subir'},
            {id: 'completed', name: 'Subidos'}, {id: 'error', name: 'Errores'}];
        return (
            <ul className="navbar-tabs group">
                {tabNames.map((el, index) => (
                    <NavElement pos={index} key={index} navId={el.id} click={this.handleNavClick.bind(this)}
                        navName={el.name} isActive={this.state[index]} />
                ))}
            </ul>
        )
    }
}

export default Navbar;