#include <BRepBuilderAPI_MakeEdge2d.hxx>
#include <BRepAlgoAPI_Cut.hxx>
#include <Geom2d_Circle.hxx>
#include <gp_Circ2d.hxx>

int main(int argc, char **argv){
    TopoDS_Shape c1,c2;
    c1 = BRepBuilderAPI_MakeEdge2d( Geom2d_Circle( gp::OX2d(), 1 ).Circ2d() ).Shape();
    c2 = BRepBuilderAPI_MakeEdge2d( Geom2d_Circle( gp::OX2d(), 2 ).Circ2d() ).Shape();
    BRepAlgoAPI_Cut cut(c1,c2);
    cut.RefineEdges();
    return 1;
}
