import os
import cv2

def generate_video(images, nv_dossier, im_dossier, num):
    video_name = 'video_' + str(num) + '.avi' 
    os.chdir(nv_dossier)
    
    frame = cv2.imread(os.path.join(im_dossier, images[0]))
    print(type(frame))
    
    height, width, layers = frame.shape  

    video = cv2.VideoWriter(video_name, 0, 1, (width, height)) 
  
    for image in images: 
        video.write(cv2.imread(os.path.join(im_dossier, image))) 
      
    cv2.destroyAllWindows() 
    video.release()
    os.chdir('..')


def regrouper_image(im_dossier, nv_dossier):
    image = os.listdir(im_dossier)
    os.makedirs(nv_dossier, exist_ok = True)
    li = []
    for i in range(1,413):
        nouvelle_liste = []
        nom_frames = 'c_'+str(i)+'_v'
        for ii in range(len(image)): 
            if nom_frames in image[ii]:
                nouvelle_liste.append(image[ii])
        if nouvelle_liste != []:
            generate_video(nouvelle_liste, nv_dossier, im_dossier, i)


regrouper_image("C:/Users/hamri/OneDrive/Bureau/projet M1/ENID_v1.0_tracked/frames/",'video/')
