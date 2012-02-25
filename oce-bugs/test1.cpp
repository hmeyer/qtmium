/*
compile like
g++ test1.cpp -o test1 -I /usr/include/oce/ -lTKBRep -lTKernel -lTKMath -lTKG2d -lTKPrim -lTKTopAlgo

*/

#include <BRepBuilderAPI_MakeEdge2d.hxx>
#include <BRepAlgo.hxx>
#include <BRepAlgo_BooleanOperation.hxx>
#include <BRepAlgo_Fuse.hxx>

#include <Geom2d_Circle.hxx>
#include <TopoDS.hxx>
#include <TopoDS_Shape.hxx>
#include <TopoDS_Edge.hxx>
#include <gp.hxx>
#include <gp_Circ2d.hxx>


int main(int argc, char **argv){
    TopoDS_Shape c1;
    TopoDS_Shape c2;
    
    c1 = BRepBuilderAPI_MakeEdge2d( Geom2d_Circle( gp::OX2d(), 1 ).Circ2d() ).Shape();
    c2 = BRepBuilderAPI_MakeEdge2d( Geom2d_Circle( gp::OX2d(), 2 ).Circ2d() ).Shape();
//    BRepAlgo_Fuse(c1,c2);
    return 1;
}
