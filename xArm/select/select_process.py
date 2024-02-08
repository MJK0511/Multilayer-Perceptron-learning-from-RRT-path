import os
from extract_middle import GenerateMiddle
from plot import Plot
from range import RangeofVal

if __name__ == "__main__":
    extractor = GenerateMiddle()
    plotter = Plot()
    selector = RangeofVal()

    default_path = "/home/nishidalab07/github/6dimension/simulation2/"
    
    input_directory = os.path.join(default_path, f'Task/extract_angle/sample')
    # input_directory = os.path.join(default_path, f'Task/plus/sample')
    # input_directory = os.path.join(default_path, f'Task/minus')
    # input_directory = os.path.join(default_path, f'Task/After_train/allpath')
    output_directory = default_path

    m = extractor.extract_m(input_directory)
    
    new_df = selector.rangeofval(m)
    # extractor.savetocsv(m, output_directory, 'm') 
    # plotter.plot_3d(extractor.m_df)
    plotter.plot_2d(extractor.m_df)
    # plotter.plot_2d(new_df)
    

    
    extractor.savetocsv(new_df, output_directory, 'selected')
    selector.copy_files(default_path)