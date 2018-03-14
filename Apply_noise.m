function  = Apply_Noise( input_dir, output_dir )
%APPLYNOISE Summary of this function goes here
%   applys noise to images in input dir to output dir
%   the output images' name will be in the format label_name.png
%   labels are
%   0 --> salt and pepper
%   1 --> gaussian
%   2 --> speckle
%   3 --> non-gaussian (not implemented yet


%% start the code
images_dir=input_dir;
    out_dir=output_dir;
    images_ext='*.png';
    images=dir(fullfile(images_dir,images_ext));

    mkdir(output_dir)
    
    for im = images'
        image=imread(strcat(images_dir,'\',im.name));
        %imshow(image);
        
        imsalt=imnoise(image,'salt & pepper');
        imgaus=imnoise(image,'gaussian');
        imspec=imnoise(image,'speckle');
    
        imwrite(imsalt,strcat(out_dir,'\0_',im.name));
        imwrite(imgaus,strcat(out_dir,'\1_',im.name));
        imwrite(imspec,strcat(out_dir,'\2_',im.name));
    end

end

