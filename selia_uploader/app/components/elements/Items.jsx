import React from 'react';
import setHours from "date-fns/setHours";
import setMinutes from "date-fns/setMinutes";
import setSeconds from "date-fns/setSeconds";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import DatePicker from 'react-datepicker';
import classNames from 'classnames';

import { faCheckCircle } from '@fortawesome/free-regular-svg-icons';
import { faCircle } from '@fortawesome/free-regular-svg-icons';

import { useSelector, useDispatch } from 'react-redux';

function Items(props) {
    const items = useSelector(state => state.items.items);
    const dispatch = useDispatch();
    const onClick = (file) => {
        dispatch({
            type: 'CHANGE_ITEM',
            payload: file
        })
    }
    return (
        <ul id={props.idDiv} className={classNames(
                'statusDiv',
                { hidden: props.position >= 1 ? true : false }
            )}>
            {items.map((item, index) => {
                if(item.status.value == props.idDiv) {
                    return (
                        <li key={index}>
                                {item.selected ? 
                                        <FontAwesomeIcon icon={faCheckCircle} onClick={() => onClick(item)}/> : 
                                        <FontAwesomeIcon icon={faCircle} onClick={() => onClick(item)}/>}
                                <p>{item.file}</p>
                                <input tipe="text" placeholder={item.device}/>
                                <DatePicker
                                  selected={new Date(item.date)}
                                  onChange={date => setStartDate(date)}
                                  showTimeSelect
                                  minTime={setHours(setMinutes(setSeconds(new Date(), 0), 0), 17)}
                                  maxTime={setHours(setMinutes(setSeconds(new Date(), 5), 5), 20)}
                                  dateFormat="dd/MM/yy h:mm:ss"
                                />
                                <p>{item.status ? item.status.name : null}</p>
                        </li>)
                    }
                }
            )}
        </ul>
    )
}

export default Items;