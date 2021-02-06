import { getInfo } from 'react-mediainfo'

export const imageMediaInfo = {
    "image_width": 200,
    "image_length": 200,
    "datetime_original": new Date().toISOString()
}

export default {
    async getMediaInfo(file) {
        if(file.type.includes('audio')){
            const mediaInfo = await getInfo(file);
            let metadata = mediaInfo.media.track[1];
            let audioMediaInfo = {
                "frames": parseInt(metadata.SamplingCount),
                "channels": parseInt(metadata.Channels),
                "duration": parseFloat(metadata.Duration),
                "sampwidth": parseInt(metadata.BitDepth)/8,
                "sampling_rate": parseInt(metadata.SamplingRate)
            };
            return audioMediaInfo;
        } else if (file.type.includes('image')) {
            return imageMediaInfo;
        }
    }
}