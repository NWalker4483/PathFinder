#include "opencv2/core/core.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "iostream"
 
using namespace cv;
using namespace std;

void filter_region(Mat image, float vertices){

        //Create the mask using the vertices and apply it to the input image
        Mat mask = mask.zeros(image.rows,image.cols,CV_8UC1);
        if ((mask.shape().size())==2){
            fillPoly(mask, vertices, 255);
            }
        else{
            fillPoly(mask, vertices, (255,)*mask.shape[2]); 
            // in case, the input image has a channel dimension        
        return bitwise_and(image, mask);
        }};
void select_region(Mat _image){
       // It keeps the region surrounded by the `vertices` (i.e. polygon).  Other area is set to 0 (black).
    	int cols,rows;
    	float top_right, bottom_right, top_left, bottom_left;
    	float vertices[[]];
        // first, define the polygon by vertices
        rows, cols = _image.rows,_image.cols;
        bottom_left  = [cols*0.1, rows*0.95];
        top_left     = [cols*0.4, rows*0.6];
        bottom_right = [cols*0.9, rows*0.95];
        top_right    = [cols*0.6, rows*0.6];
        // the vertices are an array of polygons (i.e array of arrays) and the data type must be integer
        vertices = [[bottom_left, top_left, top_right, bottom_right]];
        return filter_region(_image, vertices);
        };  
      
int main(int argc, char** argv )
{
    Mat src;
    Mat ndr;
    src = imread(argv[1], CV_LOAD_IMAGE_COLOR);
    namedWindow( "Original image", CV_WINDOW_AUTOSIZE );
    medianBlur(src,ndr,(5,5));
    cout<<ndr.size;
    imshow( "Original image", ndr);
 
    Mat gray, edge, draw;
    cvtColor(src, gray, CV_BGR2GRAY);

   // Canny operator
   
    Canny( gray, edge, 50, 150, 3);
    namedWindow("canny", CV_WINDOW_AUTOSIZE);
    imshow("canny", edge);
 

    waitKey(0);                                       
    return 0;
} 