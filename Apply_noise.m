images_dir='Camera Roll\';
images_ext='*.jpg';
images=dir(fullfile(images_dir,images_ext));

mkdir('Salt & pepper noise')
mkdir('Gaussian noise')
mkdir('Non-Gaussian noise')
mkdir('Speckle noise')

for im = images'

    image=imread(strcat(images_dir,im.name));
    imshow(image);
        
    imsalt=imnoise(image,'salt & pepper');
    imgaus=imnoise(image,'gaussian');
    imspec=imnoise(image,'speckle');
    
    imwrite(imsalt,strcat('Salt & pepper noise\',im.name));
    imwrite(imsalt,strcat('gaussian noise\',im.name));
    imwrite(imsalt,strcat('Speckle noise\',im.name));
end
