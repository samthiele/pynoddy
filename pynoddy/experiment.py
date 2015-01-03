'''Collection of classes and methods for Noddy experiments
Created on Nov 29, 2014

**Idea**: define Experiment classes to combine history and output methods into
one object for more flexibility;
Also, define additional methods for more "complex" experiments, e.g.:

- sensitivity analysis
- uncertainty analysis/ quantification/ visualisation
- inversion?

Note: use new-style class definitions throughout

@author: flohorovicic
'''
import numpy as np

import history
import output

class C(object):
    def getx(self): return self.__x
    def setx(self, value): 
        if type(value) == int:
            self.__x = value
        else:
            print("Please provide an integer value")
    def delx(self): del self.__x
    x = property(getx, setx, delx, "I'm the 'x' property.")    


class Experiment(history.NoddyHistory, output.NoddyOutput):
    '''Noddy experiment container, inheriting from both noddy history and output methods
    
    classdocs
    '''
    pass

    def __init__(self, history=None, **kwds):
        '''Combination of input and output methods for complete kinematic experiments with NOddy
        
        **Optional Keywords**:
            - *his_file* = string : filename of Noddy history input file
        '''
        super(Experiment, self).__init__(history)
#        super(Experiment, self).test()
#        if kwds.has_key("history"):
#            self.load_history(kwds['history'])
#            print("Determine events")
#            self.determine_events()
    
    def update(self):
        """Update model computation"""
        self.set_up_to_date()
    
    def set_up_to_date(self):
        """Set boolean variable for valid object"""
        self.__is_up_to_date = True
    
    def get_up_to_date(self):
        """Get model state"""
        return self.__is_up_to_date
        
    is_up_to_date = property(get_up_to_date, set_up_to_date, None, "Model state")
            
            
    def set_parameter_statistics(self, param_stats):
        """Define parameter statistics for uncertainty simulation and sensitivity analysis
        
        param_stats = dict : dictionary with relevant statistics defined for event parameters
        dictionary is organised as:
        param_stats[event_id][parameter_name][stats_type] = value
        
        Example:
        param_stats[2]["Dip"]["min"] = 200.
        
        Possible statistics are:
            - min = float : minimum bound
            - max = float : maximum bound
            - type = 'normal', 'uniform' : distribution type
            - stdev = float : standard deviation (if normal distribution)
        """
        self.param_stats = param_stats
        
    def freeze(self, **kwds):
        """Freeze the current model state: store the event settings for later comparison"""
        self.base_events = self.copy_events()

        
    def random_perturbation(self, **kwds):
        """Perform a random perturbation of the model according to parameter statistics
        defined in self.param_stats
        
        **Optional arguments**:
            - *store_params* = bool : store random parameter set (default: True)
        """
        store_params = kwds.get("store_params", True)
        # create a dictionary for event parameter changes:
        param_changes = {}
        for param in self.param_stats:
            # assign new value, according to statistics
            param_changes[param['event']] = {}
            # get original value:
            ori_val = self.events[param['event']].properties[param['parameter']]
            # check distribution type:
            if param.has_key("type"):
                if param['type'] == 'normal':
                    # draw value of normal distribution:
                    mean = param.get("mean", ori_val) # default mean is original value
                    if not param.has_key('stdev'):
                        raise AttributeError("Please assign standard deviation value (as 'stdev' entry)!")
                    stdev = param.get("stdev")
                    random_val = np.random.normal(mean, stdev)
                    # assign relative change
                    param_changes[param['event']][param['parameter']] = random_val - ori_val
                else:
                    raise AttributeError("Sampling for type %s not yet implemented, sorry." % param['type'])
        # assign changes to model:
        self.change_event_params(param_changes)
        # store results for later analysis
        if store_params:
            if not hasattr(self, 'random_parameter_changes'):
                # initialise array
                self.random_parameter_changes = [param_changes]
            else:
                self.random_parameter_changes.append(param_changes)
        
    def shuffle_event_order(self, event_ids):
        """Randomly shuffle order of events
        
        **Arguments**:
            - *event_ids* = [list of event ids] : event ids to be randomly shuffeled
        """
        new_order = np.random.choice(event_ids, size = len(event_ids), replace=False)
        # set up reorder-dictionary
        reorder_dict = {}
        for i,ev_id in enumerate(event_ids):
            reorder_dict[ev_id] = new_order[i]
        self.reorder_events(reorder_dict)
        
    def get_sampling_line_data(self, xyz_from, xyz_to):
        """Get computed model along a line, for example as a drillhole position
        
        **Arguments**:
            - *xyz_from* = [x, y, z] : list of float values for starting position
            - *xyz_to* = [x, y, z] : list of float values for starting position
        """
        pass
    
    def plot_section(self, direction='y', position='center', **kwds):
        """Extended version of plot_section method from pynoddy.output class
        
        **Optional arguments**:
            - *resolution* = float : set resolution for section (default: self.cube_size)
            - *model_type* = 'current', 'base' : model type (base "freezed" model can be plotted for comparison)
        """
        self.get_cube_size()
        self.get_extent()
        resolution = kwds.get("resolution", self.cube_size)
        model_type = kwds.get("model_type", 'current')
        
        self.determine_model_stratigraphy()
        
        # code copied from noddy.history.HistoryFile.get_drillhole_data()
        self.get_origin()
        z_min = kwds.get("z_min", self.origin_z)
        z_max = kwds.get("z_max", self.extent_z)
        x_min = self.origin_x
        x_max = self.extent_x
        y_pos = (self.extent_y - self.origin_y - resolution) / 2. 
        # 1. create copy
        import copy
        tmp_his = copy.deepcopy(self)
        # 2. set values
        tmp_his.set_origin(x_min, y_pos, z_min) # z_min)
        tmp_his.set_extent(x_max, resolution, z_max)
        tmp_his.change_cube_size(resolution)
        
        if model_type == 'base':
            tmp_his.events = self.base_events.copy()
        
        # 3. save temporary file
        tmp_his_file = "tmp_section.his"
        tmp_his.write_history(tmp_his_file)
        tmp_out_file = "tmp_section_out"
        # 4. run noddy
        import pynoddy
        import pynoddy.output
        
        pynoddy.compute_model(tmp_his_file, tmp_out_file)
        # 5. open output
        tmp_out = pynoddy.output.NoddyOutput(tmp_out_file)
        # 6. 
        tmp_out.plot_section(layer_labels = self.model_stratigraphy, **kwds)
        # return tmp_out.block
    
class SensitivityAnalysis(Experiment):
    '''Sensitivity analysis experiments for kinematic models
    
    Sensitivity analysis with methods from the SALib package:
    https://github.com/jdherman/SALib
    '''
    from SALib.sample import saltelli
    
    def __init__(self, **kwds):
        """Sensitivity analysis for kinematic models
        
        **Optional Keywords**:
            - *his_file* = string : filename of Noddy history input file
        """
        if kwds.has_key("his_file"):
            self.load_history(kwds['his_file'])
            self.determine_events()
            
    def create_params_file(self, **kwds):
        """Create params file from defined parameter statistics for SALib analysis
        
        Note: parameter statistics have to be defined in self.param_stats dictionary
        (use self.set_parameter_statistics)
        
        Changes are expressed as relative changes of the parameter with respect to the initial value.
        
        **Optional keywords**:
            - *filename* = string : name of parameter file (default: params_file_tmp.txt)
        
        """
        
        filename = kwds.get("filename", "params_file_tmp.txt")
        
        if not hasattr(self, "param_stats"):
            raise AttributeError("Please define parameter statistics dictionary first (define with self.set_parameter_statistics) ")
        
        f = open(filename, 'w')
        
        for param in self.param_stats:
            # create a meaningful name for the parameter
            par_name = "ev_%d_%s" % (param['event'], param['parameter'].replace (" ", "_"))
            f.write("%s %f %f\n" % (par_name, param['min'] - param['initial'], param['max'] - param['initial']))
                
        f.close()
    
    def add_sampling_line(self, x, y, **kwds):
        """Define a vertical sampling line, for example as a drillhole at position (x,y)
        
        As default, the entire length for the model extent is exported. Ohter depth ranges
        can be defined with optional keywords.
        
        **Arguments**:
            - *x* = float: x-position of drillhole
           - *y* = float: y-position of drillhole
            
        **Optional keywords**:
            - *z_min* = float : minimum z-value (default: model origin)
            - *z_max* = float : maximum z-value (default: surface)
            - *label* = string : add a label to line (e.g. drillhole name, location, etc.)
        """
        if not hasattr(self, "sampling_lines"):
            self.sampling_lines= {}

        self.get_extent()
        self.get_origin()

        z_min = kwds.get("z_min", self.origin_z)
        z_max = kwds.get("z_max", self.extent_z)

        label = kwds.get('label', 'line %d' % len(self.sampling_lines))
        self.sampling_lines[label] = {'x' : x, 'y' : y, 'z_min' : z_min, 'z_max' : z_max}
            
        
    def distance(self, **kwds):
        """Calculate distance between current state and base model 
        
        The standard distance is calculated as L1 norm of relative stratigraphic difference
        along sampling lines.
        
        **Optional keywords**:
            - *norm* = 'L1', 'L2' : norm to calculate distance
            - *resolution* = float : model resolution to calculate distance at sampling lines
        """
        # First step: get data along sampling lines and append to one long array
        resolution = kwds.get("resolution", 1.0)
        
        
        # test if sampling lines are defined
        if not hasattr(self, "sampling_lines"):
            raise AttributeError("Sampling lines are required to calculate distance!")

        # get current line values:
        current_lines = self.get_model_lines(resolution = resolution)
        
        # check if model values along base line have previously been calculated 
        # and if they have the same resolution - if not, do that
        if not hasattr(self, "base_model_lines") or (len(current_lines) != len(self.base_model_lines)):
            self.get_model_lines(resolution = resolution, model_type = 'base')
        
        # calculate distance:
        distance = np.sum(np.abs(self.base_model_lines - current_lines)) / float(len(self.base_model_lines))
        
        return distance
    
    def determine_distances(self, **kwds):
        """Determine distances for a given parameter sets, based on defined sampling lines
        
        **Optional keywords**:
            - *param_values* = list of parameter values (as, for example, created by SALib methods)
            - *resolution* = float : model resolution to calculate distance at sampling lines
        """
        if kwds.has_key("param_values"):
            param_values = kwds['param_values']
        elif hasattr(self, 'param_values'):
            param_values = self.param_values
        else:
            raise AttributeError("Please define paramter values as object variable or pass as keyword argument!")
        
        # test if sampling lines are defined
        if not hasattr(self, "sampling_lines"):
            raise AttributeError("Sampling lines are required to calculate distance!")
        
        # First step: get data along sampling lines and append to one long array
        resolution = kwds.get("resolution", 1.0)
        
        distances = []
        
        # create model for each parameter set and calculate distance
        for param_set in param_values:
            param_changes = {}
            
            for i,param_val in enumerate(param_set):
                
                # order of parameters in list corresponds to entires in self.param_stats:
                param = self.param_stats[i]
                
                # initialise parameter changes dictionary if it doesn't exist:
                if not param_changes.has_key(param['event']):
                    param_changes[param['event']] = {}
                param_changes[param['event']][param['parameter']] = param_val
                
            # apply change to model:
            self.change_event_params(param_changes)

            # calculated distance to base model for given resolution
            distances.append(self.distance(resolution = resolution))
        
        return distances
    
    
    def get_model_lines(self, **kwds):
        """Get base model along the defined sampling lines
        
        **Optional keywords**:
            - *model_type* = 'base', 'current' : model type (select base to get freezed model)
            - *resolution* = float : model resolution to calculate distance at sampling lines
        """
        resolution = kwds.get("resolution", 1)
        model_type = kwds.get("model_type", 'current')
        
        import copy

        tmp_his = copy.deepcopy(self)
        
        current_lines = np.array([])
        # get model for all sampling lines
        for sl in self.sampling_lines.values():
            # 2. set values
            tmp_his.set_origin(sl['x'], sl['y'], sl['z_min'])
            tmp_his.set_extent(resolution, resolution, sl['z_max'])
            tmp_his.change_cube_size(resolution)
            
            # test if base model:
            if model_type == 'base':
                # set base events:
                tmp_his.events = self.base_events.copy()
                
            elif model_type == 'current':
                # use current model, do nothing for now
                pass
            
            else: 
                raise AttributeError("Model type %s not known, please check!" % model_type)
            
            # 3. save temporary file
            tmp_his_file = "tmp_1D_drillhole.his"
            tmp_his.write_history(tmp_his_file)
            tmp_out_file = "tmp_1d_out"
            # 4. run noddy
            import pynoddy
            import pynoddy.output
            
            pynoddy.compute_model(tmp_his_file, tmp_out_file)
            # 5. open output
            tmp_out = pynoddy.output.NoddyOutput(tmp_out_file)
            # 6. 
            current_lines = np.append(current_lines, tmp_out.block[0,0,:])
        
        # if base model: store as class variable:
        
        # test if base model:
        if model_type == 'base':
            self.base_model_lines = current_lines
        
        return current_lines
    











        
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        
        