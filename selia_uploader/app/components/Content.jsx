import React from 'react';
import classNames from 'classnames';

function Items({ idDiv, listElements, position }) {
    return (
        <ul id={idDiv} className={classNames(
                'statusDiv',
                { hidden: position >= 1 ? true : false }
            )}>
            {listElements.map((el, index) => (
                <li key={index}>
                    {el}
                </li>
            ))}
        </ul>
    )
}


function Content() {
    let itemStatus = [
        {
            name: 'preview',
            elements: ['item1','item2','item3']
        },
        {   
            name: 'uploading',
            elements: ['item1']
        },
        {
            name: 'completed',
            elements: ['item2']
        },
        {
            name: 'error',
            elements: ['item3']
        }];
    return (
        <div id="content">
            {itemStatus.map((item, index) => (
                <Items key={index} idDiv={item.name} position={index}
                        listElements={item.elements}/>
            ))}
        </div>
    )
}

export default Content;