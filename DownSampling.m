%% Read Dataset
input_directory = 'D:/GP/Datasets/training/SR_training_datasets/General100/'; % input images
output_directory = 'C:/Users/amr/Desktop/GP downsampled/'; % output images
filenames = dir(fullfile(input_directory, '*.png'));

num_images = length(filenames); %number of images found in selected folder

for i = 1:num_images
    %Build File Name
    filename = fullfile(input_directory, filenames(i).name);
    %Read Colored Image of 'filename'
    image = imread(filename);
    Xdown = image(1:8:end,1:8:end,:);
    outname = fullfile(output_directory, filenames(i).name);
    imwrite(Xdown,outname);
end