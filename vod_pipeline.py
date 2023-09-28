from vod_download import download_vod, crop_vod_to_minimap
from vod_mask import add_mask
import asyncio
import os

async def main() -> None:
    vod_map = 'split'
    vod_path, vod_resolution = await download_vod(
        url="https://www.youtube.com/watch?v=fB8Uxe0JEXw&list=PLMJ9cfx_WDdybdHDw28uCEFnxQvprJ59W&t=461s", 
        verbose=True
    )

    await crop_vod_to_minimap(
        vod_path=vod_path, 
        vod_resolution=vod_resolution, 
        vod_start='00:07:41 ',
        vod_end='00:08:24',
    )

    # os.remove(vod_path+'.mp4')
    
    add_mask(vod_path=vod_path+'_EDITED.mp4', vod_map=vod_map, out_path=vod_path+'_FINAL.mp4')
    # os.remove(vod_path+'_EDITED.mp4')

if __name__ == '__main__':
    asyncio.run(main())