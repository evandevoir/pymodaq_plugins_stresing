import numpy as np
from pathlib import Path

from pymodaq_utils.utils import ThreadCommand
from pymodaq_data.data import DataToExport, Axis
from pymodaq_gui.parameter import Parameter

from pymodaq.control_modules.viewer_utility_classes import DAQ_Viewer_base, comon_parameters, main
from pymodaq.utils.data import DataFromPlugins


#  Here we suppose that the wrapper is in the hardware/stresing directory.
from pymodaq_plugins_stresing.hardware import stresing

#Read the config.ini file given by Stresing. We assume it is in located in the hardware folder
config_path = Path(stresing.__file__).parent.parent / "config.ini"
config = stresing.load_config_file(str(config_path))
drvno = 0 #do not change that except is you have different PCIE board

class DAQ_1DViewer_FLCC3001(DAQ_Viewer_base):
    """ Instrument plugin class for a 1D viewer.
    
    This object inherits all functionalities to communicate with PyMoDAQ’s DAQ_Viewer module through inheritance via
    DAQ_Viewer_base. It makes a bridge between the DAQ_Viewer module and the Python wrapper of a particular instrument.

    TODO Complete the docstring of your plugin with:
        * The set of instruments that should be compatible with this instrument plugin.
        * With which instrument it has actually been tested.
        * The version of PyMoDAQ during the test.
        * The version of the operating system.
        * Installation instructions: what manufacturer’s drivers should be installed to make it run?

    Attributes:
    -----------
    controller: object
        The particular object that allow the communication with the hardware, in general a python wrapper around the
         hardware library.
         
    # TODO add your particular attributes here if any

    """
    params = comon_parameters+[
        {'title': 'Acquisition Settings:', 'name': 'acq_settings', 'type': 'group', 'children': [

                {'title': 'Number of samples:', 'name': 'nos', 'type': 'int', 'value': 2, 'default': 2, 'min': 2, 'max':4294967295},
                {'title': 'Number of blocks:', 'name': 'nob', 'type': 'int', 'value': 1, 'default': 1, 'min': 1, 'max':4294967295},
                {'title': 'Continuous measurment:', 'name': 'cont_meas', 'type': 'bool', 'value': False},
                {'title': 'Pause between two acquisitions (us):', 'name': 'int', 'type': 'int', 'value': 0, 'default': 0, 'min': 0, 'max':4294967295},

        ]}
        ]

    def ini_attributes(self):

        self.controller: stresing = None
        self.x_axis = None
        super().ini_attributes()

    def ini_detector(self, controller=None):
        """Detector communication initialization

        Parameters
        ----------
        controller: (object)
            custom object of a PyMoDAQ plugin (Slave case). None if only one actuator/detector by controller
            (Master case)

        Returns
        -------
        info: str
        initialized: bool
            False if initialization failed otherwise True
        """

        if self.is_master:
            self.controller = stresing.init_driver()  #initiate the driver
            initialized = isinstance(self.controller, int) and self.controller > 0 #True if at least one board is detected
        else:
            self.controller = controller
            initialized = True


        # get the x_axis (you may want to do this also in the commit settings if x_axis may have changed
        n_pixels = int(stresing.settings.camera_settings[drvno].pixel) #read in the file the pixel channel
        data_x_axis = np.arange(n_pixels)
        self.x_axis = Axis(data=data_x_axis, label='Pixel', units='pixel', index=0)


        self.dte_signal_temp.emit(DataToExport(name='stresing',
                                               data=[DataFromPlugins(name='Cameras',
                                                                     data=[np.zeros(n_pixels),
                                                                           np.zeros(n_pixels)],
                                                                     dim='Data1D', labels=['Channel A', 'Channel B'],
                                                                     axes=[self.x_axis])]))

        info = "Intialization of the cameras."
        return info, initialized

    def close(self):
        """Terminate the communication protocol"""
        # only the master owns the controller (a slave must not close the shared one) and ini_stage/ini_detector may
        # have failed before creating it, so close can be called while self.controller is still None
        if self.is_master and self.controller is not None:
            self.controller.exit_driver()

    def grab_data(self):
        """Start a grab from the detector
        """
        ##synchrone version (blocking function)
        self.controller.init_measurement()
        self.controller.start_measurement_blocking()
        frame_buffer_2d = self.controller.copy_all_data_2d(drvno=drvno)
        avgA = np.mean([row for i, row in enumerate(frame_buffer_2d) if i % 2 == 0], axis=0) #Channel A
        avgB = np.mean([row for i, row in enumerate(frame_buffer_2d) if i % 2 == 1], axis=0) #Channel B
        data_tot = np.vstack((avgA, avgB))
        self.dte_signal.emit(DataToExport('stresing',
                                          data=[DataFromPlugins(name='Cameras', data=data_tot,
                                                                dim='Data1D', labels=['Channel A', 'Channel B'],
                                                                axes=[self.x_axis])]))

        """
        ##asynchrone version (non-blocking function with callback)
        self.controller.start_measurement_nonblocking()
        #########################################################
        """
    '''    
    def callback(self):
        """optional asynchrone method called when the detector has finished its acquisition of data"""
        data_tot = self.controller.copy_all_data_2d(drvno=drvno)
        self.dte_signal.emit(DataToExport('myplugin',
                                          data=[DataFromPlugins(name='Mock1', data=data_tot,
                                                                dim='Data1D', labels=['dat0', 'data1'])]))
    '''

    def stop(self):
        """Stop the current grab hardware wise if necessary"""
        self.controller.abort_measurement()
        self.emit_status(ThreadCommand('Update_Status', ['Acquisition manually aborted']))
        ##############################
        return ''

    def commit_settings(self, param: Parameter):
        """Apply the consequences of a change of value in the detector settings

        Parameters
        ----------
        param: Parameter
            A given parameter (within detector_settings) whose value has been changed by the user
        """
        '''
        ## TODO for your custom plugin
        if param.name() == "a_parameter_you've_added_in_self.params":
           self.controller.your_method_to_apply_this_param_change()
#        elif ...
        ##
        '''

if __name__ == '__main__':
    main(__file__)
