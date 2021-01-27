import moment from 'moment-timezone';

export default {
    getTimeZones(date) {
        const tzNames = moment.tz.names();
        const map = new Map();

        for (const name of tzNames) {
          const offsets = moment.tz.zone(name).offsets;
        
          for (const offset of offsets) {
              if (!map.has(offset)) {
                  map.set(offset, new Set);
              }
          
              map.get(offset).add(name);
          }
        }

        const currentOffset = new Date(date).getTimezoneOffset();
        const offsetList = [];
        for(let item of map.get(currentOffset))
            offsetList.push(item)

        return offsetList;
    }
}