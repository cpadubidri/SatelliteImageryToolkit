from arcpy.management import CreatePansharpenedRasterDataset
from arcpy import Exists
import os
from datetime import datetime


class Pansharpen():
    def __init__(self):
        pass

    
    def arcpy_pansharpen(self,in_ms_path, in_pan_path,out_ps_path,  msred_channel="3", msgreen_channel="2", msblue_channel="1", msinfrared_channel="4", pansharpening_type="Gram-Schmidt", 
                        red_weight="0.39", green_weight="0.23", blue_weight="0.21", infrared_weight="0.17", sensor="WorldView-2"):
        
        #Pan and Multi spectral sanity check
        if not self.__validate_tif__(in_ms_path, in_pan_path):
            return False
        print(out_ps_path)
        if not os.path.exists(os.path.dirname(out_ps_path)):
            print("Given Outpath Not exists")
            return False
        try:
            print(f'Processing : {in_ms_path}')
            CreatePansharpenedRasterDataset(in_raster=in_ms_path, in_panchromatic_image=in_pan_path, \
                                            red_channel=msred_channel, green_channel=msgreen_channel, blue_channel=msblue_channel, infrared_channel=msinfrared_channel, \
                                            out_raster_dataset=out_ps_path, \
                                            pansharpening_type=pansharpening_type, \
                                            red_weight=red_weight, green_weight=green_weight, blue_weight=blue_weight, infrared_weight=infrared_weight, \
                                            sensor=sensor)
            return True
        except Exception as e:
            print(f"Failed to create pansharpened dataset: {str(e)}")
            return False

    def batch_pansharpen(self, in_ms_folderpath, in_pan_folderpath, out_ps_folderpath):
        image_list = [file for file in os.listdir(in_ms_folderpath) if file.endswith('.TIF')]

        for image in image_list:
            start_time = datetime.now()
            in_ms_path = os.path.join(in_ms_folderpath,image)
            in_pan_path = os.path.join(in_pan_folderpath,image.replace('M','P'))
            out_ps_path = os.path.join(out_ps_folderpath, image)
            print(out_ps_path)
            status = self.arcpy_pansharpen(in_ms_path, in_pan_path, out_ps_path)

            if status:
                print("Pansharpened dataset created successfully. ")
            else:
                print(f"{image} Pansharpened Failled !!!!!")

            end_time = datetime.now()
            execution_time = end_time - start_time
            print(f"Execution time: {execution_time}")
            print("#######################################################################")


    def __validate_tif__(self, *paths):
        for path in paths:
            if not Exists(path):
                print(f"Error: {path} - Path does not exist")
                return False
            else:
                pass
        return True




if __name__=="__main__":
    # Pansharpen().arcpy_pansharpen(in_ms_path=r'data\ms\24APR01083715-M2AS_R1C1-050209502010_01_P001.TIF', \
    #                                    in_pan_path=r'data\pn\24APR01083715-P2AS_R1C1-050209502010_01_P001.TIF', \
    #                                    out_ps_path = r'data/ps/test.TIF')

    in_ms_folderpath = r'data\ms'
    in_pan_folderpath = r'data\pn'
    out_ps_folderpath = r'data\ps'

    Pansharpen().batch_pansharpen(in_ms_folderpath, in_pan_folderpath, out_ps_folderpath)
    

