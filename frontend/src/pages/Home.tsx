import React from "react";
import { TableBlock } from "../components/runtime/TableBlock";
import { MethodButton } from "../components/MethodButton";

const Home: React.FC = () => {
  return (
    <div id="qW1ndOj3OJpILq7m">
    <div id="i07fk-2" className="gjs-row" style={{"width": "100%", "paddingTop": "10px", "paddingRight": "10px", "paddingBottom": "10px", "paddingLeft": "10px", "display": "flex", "--chart-color-palette": "default", "flexWrap": "wrap"}} />
    <nav id="i3znv" style={{"padding": "15px 30px", "fontFamily": "Arial, sans-serif", "display": "flex", "color": "white", "backgroundImage": "linear-gradient(#234df8 0%, #234df8 100%)", "backgroundSize": "auto", "backgroundPosition": "left top", "backgroundRepeat": "repeat", "--chart-color-palette": "default", "justifyContent": "space-between", "alignItems": "center"}}>
      <p id="ipkss" style={{"fontSize": "24px", "fontWeight": "bold", "--chart-color-palette": "default"}}>{"H-Index Predictor"}</p>
      <div id="i9ra6" style={{"display": "flex", "--chart-color-palette": "default", "gap": "30px"}} />
    </nav>
    <div id="iewj-2" style={{"padding": "0px 20px 10px 20px", "minHeight": "80px", "color": "black", "opacity": "1", "border": "1px solid #4f5155", "backgroundImage": "linear-gradient(#55575c 0%, #55575c 100%)", "backgroundSize": "auto", "backgroundPosition": "left top", "backgroundRepeat": "repeat", "--chart-color-palette": "default"}}>
      <section id="container_section" className="bdg-sect">
        <h1 id="h1" className="heading" style={{"color": "#ffffff", "--chart-color-palette": "default"}}>{"Predict Your H-Index in 5 Years"}</h1>
      </section>
      <p id="i2el6" style={{"padding": "10px 0px 10px 0px", "margin": "0px 100px 0px -1px", "fontSize": "large", "fontWeight": "500", "color": "#ffffff", "--chart-color-palette": "default"}}>{"Enter your current academic metrics below and get an AI-powered forecast."}</p>
    </div>
    <div id="ike7h" style={{"padding": "20px", "display": "flex", "--chart-color-palette": "default", "flexDirection": "column", "gap": "20px"}} />
    <TableBlock id="iwvuy" styles={{"width": "100%", "minHeight": "400px", "--chart-color-palette": "default"}} title="Your Academic Profile" options={{"showHeader": true, "stripedRows": false, "showPagination": true, "rowsPerPage": 5, "actionButtons": true, "columns": [{"label": "HIndex", "column_type": "field", "field": "hIndex", "type": "int", "required": true}, {"label": "TotalCitations", "column_type": "field", "field": "totalCitations", "type": "int", "required": true}, {"label": "TotalPapers", "column_type": "field", "field": "totalPapers", "type": "int", "required": true}, {"label": "CareerAge", "column_type": "field", "field": "careerAge", "type": "int", "required": true}, {"label": "CitationsPerPaper", "column_type": "field", "field": "citationsPerPaper", "type": "float", "required": true}], "formColumns": [{"column_type": "field", "field": "totalPapers", "label": "totalPapers", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "careerAge", "label": "careerAge", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "citationsPerPaper", "label": "citationsPerPaper", "type": "float", "required": true, "defaultValue": null}, {"column_type": "field", "field": "hIndex", "label": "hIndex", "type": "int", "required": true, "defaultValue": null}, {"column_type": "field", "field": "totalCitations", "label": "totalCitations", "type": "int", "required": true, "defaultValue": null}, {"column_type": "lookup", "path": "researchfield", "field": "researchfield", "lookup_field": "name", "entity": "ResearchField", "type": "str", "required": true}]}} dataBinding={{"entity": "Researcher", "endpoint": "/researcher/"}} />
    <div id="inzll" className="gjs-row" style={{"width": "100%", "padding": "10px", "display": "flex", "--chart-color-palette": "default", "flexWrap": "wrap"}}>
      <div id="iq2ej" className="gjs-cell" style={{"height": "auto", "--chart-color-palette": "default", "flex": "1 1 calc(33.333% - 20px)", "minWidth": "250px"}}>
        <MethodButton id="i2r7b" className="action-button-component" style={{"padding": "6px 14px", "fontSize": "13px", "fontWeight": "600", "textDecoration": "none", "letterSpacing": "0.01em", "display": "flex", "cursor": "pointer", "transition": "background 0.2s", "background": "linear-gradient(90deg, #f59e0b 0%, #d97706 100%)", "color": "#fff", "borderRadius": "4px", "border": "none", "boxShadow": "0 1px 4px rgba(245,158,11,0.10)", "--chart-color-palette": "default", "alignItems": "center"}} endpoint="/researcher/{researcher_id}/methods/predict/" label="Predict My H-Index in 5 Years" isInstanceMethod={true} instanceSourceTableId="iwvuy" />
      </div>
      <div id="iomaf" className="gjs-cell" style={{"height": "75px", "--chart-color-palette": "default", "flex": "1 1 calc(33.333% - 20px)", "minWidth": "250px"}} />
      <div id="i7sfh" className="gjs-cell" style={{"height": "75px", "--chart-color-palette": "default", "flex": "1 1 calc(33.333% - 20px)", "minWidth": "250px"}} />
    </div>
    <footer id="ix5hg" style={{"padding": "40px 20px", "fontFamily": "Arial, sans-serif", "color": "white", "backgroundImage": "linear-gradient(#1a59dd 0%, #1a59dd 100%)", "--chart-color-palette": "default"}}>
      <div id="i6mip" style={{"margin": "0 auto", "maxWidth": "1200px", "display": "grid", "--chart-color-palette": "default", "gap": "30px", "gridTemplateColumns": "repeat(auto-fit, minmax(250px, 1fr))"}}>
        <div id="Component">
          <h4 id="i739i" style={{"marginTop": "0", "--chart-color-palette": "default"}}>{"About This Tool"}</h4>
          <p id="i4e4o" style={{"lineHeight": "1.6", "color": "#ffffff", "opacity": "0.8", "--chart-color-palette": "default"}}>{"H-Index Predictor uses neural networks and Semantic Scholar data to forecast your academic impact 5 years ahead."}</p>
        </div>
        <div id="itgxp">
          <ul id="i82az" style={{"padding": "0", "opacity": "0.8", "--chart-color-palette": "default"}} />
        </div>
        <div id="Component_2">
          <h4 id="il1d9">{"Contact"}</h4>
          <p id="i342l" style={{"opacity": "0.8", "--chart-color-palette": "default"}}>{"Email: info@besser-pearl.org"}</p>
        </div>
      </div>
      <p id="iqa2q" style={{"paddingTop": "20px", "marginTop": "30px", "textAlign": "center", "opacity": "0.7", "borderTop": "1px solid rgba(255,255,255,0.1)", "--chart-color-palette": "default"}}>{"© 2025 BESSER. All rights reserved."}</p>
    </footer>    </div>
  );
};

export default Home;
