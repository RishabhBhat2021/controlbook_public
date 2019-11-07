classdef dataPlotterObserver < handle
    properties
        % data histories
        time_history
        theta_history
        theta_hat_history
        theta_dot_history
        theta_hat_dot_history
        index
        % figure handles
        theta_handle
        theta_hat_handle
        theta_dot_handle
        theta_hat_dot_handle
    end
    methods
        %--constructor--------------------------
        function self = dataPlotterObserver(P)
            % Instantiate lists to hold the time and data histories
            self.time_history = NaN*ones(1,(P.t_end-P.t_start)/P.t_plot);
            self.theta_history = NaN*ones(1,(P.t_end-P.t_start)/P.t_plot);
            self.theta_hat_history = NaN*ones(1,(P.t_end-P.t_start)/P.t_plot);
            self.theta_dot_history = NaN*ones(1,(P.t_end-P.t_start)/P.t_plot);
            self.theta_hat_dot_history = NaN*ones(1,(P.t_end-P.t_start)/P.t_plot);
            self.index = 1;

            % Create figure and axes handles
            figure(3), clf
            subplot(2, 1, 1)
                hold on
                self.theta_handle = plot(self.time_history, self.theta_history, 'b');
                self.theta_hat_handle = plot(self.time_history, self.theta_hat_history, 'g');
                ylabel('theta(deg)')
                title('Arm State and Observed State')
            subplot(2, 1, 2)
                hold on
                self.theta_dot_handle = plot(self.time_history, self.theta_dot_history, 'b');
                self.theta_hat_dot_handle = plot(self.time_history, self.theta_hat_dot_history, 'g');
                ylabel('thetadot(deg/s)')
        end
        
        function self = update(self, t, x, xhat)
            % update the time history of all plot variables
            self.time_history(self.index) = t;
            self.theta_history(self.index) = 180/pi*x(1);
            self.theta_dot_history(self.index) = 180/pi*x(2);
            self.theta_hat_history(self.index) = 180/pi*xhat(1);
            self.theta_hat_dot_history(self.index) = 180/pi*xhat(2);
            self.index = self.index + 1;
            % update the plots with associated histories
            set(self.theta_handle, 'Xdata', self.time_history, 'Ydata', self.theta_history)
            set(self.theta_dot_handle, 'Xdata', self.time_history, 'Ydata', self.theta_dot_history)
            set(self.theta_hat_handle, 'Xdata', self.time_history, 'Ydata', self.theta_hat_history)
            set(self.theta_hat_dot_handle, 'Xdata', self.time_history, 'Ydata', self.theta_hat_dot_history)
        end
    end
end
