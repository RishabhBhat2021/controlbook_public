classdef armController < handle
    %----------------------------
    properties
        m
        ell
        g
        K
        kr
        limit
        Ts
    end
    %----------------------------
    methods
        %----------------------------
        function self = armController(P)
            % plant parameters known to controller
            self.m = P.m;
            self.ell = P.ell;
            self.g = P.g;
            self.K = P.K;
            self.kr = P.kr;
            self.limit = P.tau_max;
            self.Ts = P.Ts;
        end
        %----------------------------
        function tau = update(self, theta_r, x)
            theta = x(1);
            % compute feedback linearizing torque
            tau_fl = self.m*self.g*(self.ell/2)*cos(theta);           
            % Compute the state feedback controller
            tau_tilde = -self.K*x + self.kr*theta_r;
            % compute total torque
            tau = self.saturate( tau_fl + tau_tilde);
        end
        %----------------------------
        function out = saturate(self,u)
            if abs(u) > self.limit
                u = self.limit*sign(u);
            end
            out = u;
        end        
    end
end