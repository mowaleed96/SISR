function  Apply_Noise( input_dir, output_dir )
%APPLYNOISE Summary of this function goes here
%   applys noise to images in input dir to output dir
%   the output images' name will be in the format label_name.png
%   labels are
%   0 --> salt and pepper
%   1 --> gaussian
%   2 --> speckle
%   3 --> non-gaussian

%% start the code
images_dir=input_dir;
    out_dir=output_dir;
    images_ext='*.png';
    images=dir(fullfile(images_dir,images_ext));

    mkdir(output_dir)
    
    for im = images'
        %reading the image
        image=imread(strcat(images_dir,'\',im.name));
        
        %% apply first 3 noises using builtin matlab func 
        imsalt=imnoise(image,'salt & pepper');
        imgaus=imnoise(image,'gaussian');
        imspec=imnoise(image,'speckle');
    
        %% apply non-gaussian noise
        sigma=sqrt(0.01);
        mu=0;
        
        imnongaus=im2double(image);
        [size_1,size_2,size_3]=size(imnongaus);
        
        %generating a random gaussian distrubution
        array_gaussian_noise_1=randn(size_1,size_2)*sigma + mu;
        array_gaussian_noise_2=mu+randn(size_1,size_2)*sigma;
        array_gaussian_noise_3=mu+randn(size_1,size_2)*sigma;
        
        %changing the random gaussian distrubution into non-gussian one
        rray_gaussian_noise_1=[,];
        rray_gaussian_noise_2=[,];
        rray_gaussian_noise_3=[,];
        
        for i = 1:size_1
            rray_gaussian_noise_1=[rray_gaussian_noise_1; MBHTM(array_gaussian_noise_1(i,:),0.5,4)];
            rray_gaussian_noise_2=[rray_gaussian_noise_2; MBHTM(array_gaussian_noise_2(i,:),0.5,4)];
            rray_gaussian_noise_3=[rray_gaussian_noise_3; MBHTM(array_gaussian_noise_3(i,:),0.5,4)];
        end
        
        %applying the random non-gaussian distrubution noise to the image
        imnongaus(:,:,1)=imnongaus(:,:,1)+rray_gaussian_noise_1;
        imnongaus(:,:,2)=imnongaus(:,:,2)+rray_gaussian_noise_2;
        imnongaus(:,:,3)=imnongaus(:,:,3)+rray_gaussian_noise_3;
        
        %% saving the images after applying the noises
        
        imwrite(imsalt,strcat(out_dir,'\0_',im.name));
        imwrite(imgaus,strcat(out_dir,'\1_',im.name));
        imwrite(imspec,strcat(out_dir,'\2_',im.name));
        imwrite(imnongaus,strcat(out_dir,'\3_',im.name));
    end

end

