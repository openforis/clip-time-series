import geemap
from ipywidgets import Layout
import shapely.geometry as sg
import geopandas as gpd
import ee 
from utils import parameters as pm

ee.Initialize()

def setVizMap():
    
    center = [0, 0]
    zoom = 2
    
    #create the map
    m = geemap.Map(center=center, zoom=zoom)
    
    #remove everything
    m.clear_layers()
    m.clear_controls()
    
    #prevent all the handler 
    m.dragging = False
    m.keyboard = False
    m.scroll_wheel_zoom = False
    m.tap = False
    m.touch_zoom = False
    m.zoom_control = False
    m.double_click_zoom = False
    
    #define map size 
    display = Layout(width='200px', height='200px', padding="1%")
    m.layout = display
    
    return m

def setLayer(maps, pts, bands, sources):
    
    size = 2000  # 2km
    geoms = [[pts.loc[pt]['lng'], pts.loc[pt]['lat']] for pt in range(len(pts))]
    multiPoint = ee.Geometry.MultiPoint(geoms);
    
    #creates buffers
    buffer = multiPoint.buffer(size)
    
    cpt_map = 0
    ################################################
    ##     create the layers from 2005 to 2015    ##
    ################################################
    start_year = 2005
    end_year = 2016
    
    for year in range(start_year, end_year):
        if 'landsat 7' in sources:
            dataset_source = pm.getSources()['landsat 7']
            viz_band = pm.getAvailableBands()[bands][0]
            
            start = str(year) + '-01-01';
            end = str(year) + '-12-31';
            
            dataset = ee.ImageCollection(dataset_source).filterDate(start, end)
            clip = dataset.median().clip(buffer)
            
            maps[cpt_map].addLayer(clip, pm.landsatVizParam(viz_band), 'viz')
        else:
            maps[cpt_map].addLayer(buffer, {}, 'viz')
            
        cpt_map += 1
            
    ################################################
    ##     create the layers from 2016 to 2019    ##
    ################################################
    start_year = 2016
    end_year = 2020
    
    for year in range(start_year, end_year):
        start = str(year) + '-01-01';
        end = str(year) + '-12-31';
        
        if 'sentinel 2' in sources:
            dataset_source = pm.getSources()['sentinel 2']
            viz_band = pm.getAvailableBands()[bands][1]
            
            dataset = ee.ImageCollection(dataset_source).filterDate(start, end) #.filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE',20))
            clip = dataset.median().clip(buffer)
            
            maps[cpt_map].addLayer(clip, pm.sentinelVizParam(viz_band), 'viz')
        else:
            dataset_source = pm.getSources()['landsat 7']
            viz_band = pm.getAvailableBands()[bands][0]
            
            dataset = ee.ImageCollection(dataset_source).filterDate(start, end)
            clip = dataset.median().clip(buffer)
            
            maps[cpt_map].addLayer(clip, pm.landsatVizParam(viz_band), 'viz')
    
        cpt_map += 1
        
    return
    
    
    
    
    