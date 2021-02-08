/** @jsx jsx */
import { css, jsx } from '@emotion/react';
import React, { useState } from 'react';
import setHours from "date-fns/setHours";
import setMinutes from "date-fns/setMinutes";
import setSeconds from "date-fns/setSeconds";
import DatePicker from 'react-datepicker';
import { useSelector, useDispatch } from 'react-redux';

export default function AlterInfo(props) {
    const [device,setDevice] = useState('');
    const [date,setDate] = useState(new Date());
    const [timezone,setTimezone] = useState(props.items[0].timezone);
    const [changes,setChanges] = useState({});
    const dispatch = useDispatch();

    const valueChanges = (value,type) => {
        setChanges({...changes,[type]: value})
    }

    const applyToAll = () => {
        if(Object.keys(changes).length) {
            Object.entries(changes).forEach(([key,value]) => {
                for(let i=0;i<props.items.length;i++) {
                    changeFile(props.items[i],key,value)
                }
            })
        }
    }

    const changeFile = (file,field,e) => {
        dispatch({
            type: 'CHANGE_VALUE',
            payload: {
                item: file,
                field: field,
                value: e
            }
        })
    }

    return (
        <div css={css`
            position: absolute;
            bottom: calc(1em + 52px);
            width: 95%;
        `}>
            <ul css={css`
                padding: 0;
                list-style: none;
                width: 100%;
                margin: 0;
                border-top: 1px solid white;
                border-bottom: 1px solid white;
            `}>
                <li css={css`
                    padding: 5px 0px 5px 0px!important;
                    display: flex;
                    width: calc(100% - 20px);
                `}>
                    <p css={css`width: 15px!important;`}></p>
                    <p></p>
                    <input tipe="text" placeholder="Ingresa un valor" value={device} onChange={(e) => {setDevice(e.target.value);valueChanges(e.target.value,'device')}}/>
                    <DatePicker
                                  selected={date}
                                  onChange={value => {setDate(value);valueChanges(value,'date')}}
                                  showTimeSelect
                                  minTime={setHours(setMinutes(setSeconds(new Date(), 0), 0), 17)}
                                  maxTime={setHours(setMinutes(setSeconds(new Date(), 5), 5), 20)}
                                  dateFormat="dd/MM/yy h:mm:ss"
                                  popperPlacement="top-start"
                                />
                    <select className={"selectTimezone"} onChange={(e) => {setTimezone(e.target.value);valueChanges(e.target.value,'timezoneValue')}} value={timezone}>
                                    {props.items[0] ? props.items[0].timezones.map((zone, index) => (
                                        <option key={index} value={zone}>{zone}</option>
                                    )) : 
                                    <option>Sin valores</option>}
                    </select>
                    <button css={css`
                        width: calc(20% - 10px);
                        margin-left: 5px;
                        margin-right: 5px;
                        background: #dfecec;
                        color: #343a40;
                        border: none;
                        border-radius: 3px;
                    `} onClick={applyToAll}>
                        Aplicar cambios
                    </button>
                </li>
            </ul>
        </div>
    )
}