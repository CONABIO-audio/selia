import { getInfo } from 'react-mediainfo'
import exifr from 'exifr';

export default {
    async getMediaInfo(file) {
        if(file.type.includes('audio')){
            const mediaInfo = await getInfo(file);
            try {
                let metadata = mediaInfo.media.track[1];
                let audioMediaInfo = {
                    "frames": parseInt(metadata.SamplingCount),
                    "channels": parseInt(metadata.Channels),
                    "duration": parseFloat(metadata.Duration),
                    "sampwidth": parseInt(metadata.BitDepth)/8,
                    "sampling_rate": parseInt(metadata.SamplingRate)
                };
                return audioMediaInfo;
            } catch {
                return {}
            }
        } else if (file.type.includes('image')) {
            let exif = await exifr.parse(file)
            let device = exif ? exif.Make ? exif.Make : "No especificado" : "No especificado";
            let date = exif ? exif.CreateDate ? exif.CreateDate.toISOString() : exif.ModifyDate ? 
                        exif.ModifyDate.toISOString() : new Date().toISOString() : new Date().toISOString();
            try {
                let imageMediaInfo = {
                    "flash": typeof exif.Flash == "number" ? exif.Flash : null,
                    "fnumber": exif.FNumber ? String(exif.FNumber) : null,
                    "color_space": exif.ColorSpace,
                    "image_width": exif.ExifImageWidth,
                    "focal_length": exif.FocalLength ? exif.FocalLength : null,
                    "image_length": exif.ExifImageHeight,
                    "light_source": typeof exif.LightSource == "number" ? exif.LightSource : null,
                    "exposure_mode": typeof exif.ExposureMode == "number" ? exif.ExposureMode : null,
                    "exposure_time": exif.ExposureTime ? "1/" + String(Math.ceil(1/exif.ExposureTime)) : null,
                    "aperture_value": exif.ApertureValue ? String(exif.ApertureValue) : null,
                    "datetime_original": date,
                    "iso_speed_ratings": exif.ISO ? exif.ISO : null,
                    "datetime_digitized": date,
                    "max_aperture_value": exif.ApertureValue ? String(exif.ApertureValue) : null,
                    "shutter_speed_value": exif.ShutterSpeedValue ? String(exif.ShutterSpeedValue) : null
                };
                Object.keys(imageMediaInfo).forEach((key) => (imageMediaInfo[key] == null) && delete imageMediaInfo[key]); 
                return [imageMediaInfo,date,device];
            } catch {
                return [{},date,device]
            }
        } else if (file.type.includes('video')) {
            const mediaInfo = await getInfo(file);
            try {
                let metadata = mediaInfo.media.track;
                let videoMediaInfo = {
                    "audio": {
                        "channel": metadata[2].Channels,
                        "bit_rate": parseFloat(metadata[2].BitRate),
                        "sample_rate": parseInt(metadata[2].SamplingRate),
                        "bits_per_sample": parseInt(metadata[2].BitDepth),
                        "compression_rate": parseFloat(metadata[2].CodecID)
                    },
                    "video": {
                        "width": parseInt(metadata[1].Width),
                        "height": parseInt(metadata[1].Height),
                        "duration": parseInt(metadata[1].Duration),
                        "frame_rate": parseFloat(metadata[1].FrameRate),
                        "compression": metadata[1].CodecID,
                        "bits_per_pixel": parseInt(metadata[1].BitDepth)
                    },
                    "common": {
                        "width": parseInt(metadata[1].Width),
                        "height": parseInt(metadata[1].Height),
                        "bit_rate": parseFloat(metadata[1].BitRate),
                        "duration": parseInt(metadata[0].Duration),
                        "mime_type": file.type,
                        "endianness": metadata[2].Format_Settings_Endianess,
                        "frame_rate": parseFloat(metadata[0].FrameRate)
                    }
                }
                return videoMediaInfo;
            } catch {
                return {};
            }
        }
    }
}