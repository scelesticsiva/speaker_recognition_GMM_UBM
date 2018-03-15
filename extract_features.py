#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 10:13:36 2018

@author: siva
"""
import numpy as np
import copy

class extract_features(object):
    def __init__(self,window,frame_length,sampling_rate,frame_step = 10):
        self.window = np.array(window,dtype = np.float32)
        self.frame_length = frame_length
        self.frame_step = frame_step
        self.sampling_rate = sampling_rate
        self.split_frames()
        self.ZCR()
        self.RMS()
        self.fft_normalization()
        self.spectral_flux()
        self.spectral_rolloff()
        self.spectral_centroid()
        self.bandwidth()
        self.nwpd()
        self.relative_spectral_entropy()
        self.return_()
    def split_frames(self):
        self.frames = []
        samples_per_frame = int((self.frame_length*(10**-3))*self.sampling_rate)
        frame_increment = int((self.frame_step*(10**-3))*self.sampling_rate)
        index = 0
        #temp_count = 0
        while index <= len(self.window):
            if len(self.window[index:index+samples_per_frame]) == samples_per_frame:
                self.frames.append(self.window[index:index+samples_per_frame])
            index += frame_increment
        #print(temp_count)
    def ZCR(self):
        dummy_1 = copy.deepcopy(self.window)
        dummy_2 = copy.deepcopy(self.window)
        dummy_1 = np.insert(dummy_1,0,0)
        dummy_2 = np.insert(dummy_2,len(dummy_2),0)
        dummy = dummy_1*dummy_2
        self.ZCR = np.sum(dummy[1:-1]<0)/(len(self.window)-1)
#        for each in self.window:
#            if (prev_value*each) < 0:
#                count += 1
#            prev_value = each
#        self.ZCR = count/(len(self.window)-1)
        #print("ZCR:",self.ZCR)
    def RMS(self):
        RMS_entire_frame = np.sqrt(np.mean(np.square(self.window)))
        #print("RMS:",RMS_entire_frame)
        RMS_count = 0
        for each_frame in self.frames:
            RMS_current_frame = np.sqrt(np.mean(each_frame**2))
            if RMS_current_frame < 0.5*(RMS_entire_frame):
                RMS_count += 1
        #fprint("Low Energy frame rate:",RMS_count)
        self.RMS_count = RMS_count
    def fft_normalization(self):
        self.frames_fft_normalised = []
        self.frames_freq_bins = []
        self.frames_phase_angle_bins = []
        for each_frame in self.frames:
            #fft_ = np.fft.fft(each_frame)
            fft_ = np.fft.fft(each_frame,n = 512)
            fft_frame = np.absolute(fft_)
            phase_angle = np.angle(fft_,deg = True)[1:]
            #frames_freq = np.fft.fftfreq(len(each_frame),d = (1/self.sampling_rate))[1:]
            frames_freq = np.fft.fftfreq(512,d = (1/self.sampling_rate))[1:]
            fft_frame_normalised = fft_frame[1:][frames_freq>0]/(np.sum(abs(fft_frame[1:][frames_freq>0])))
            self.frames_fft_normalised.append(fft_frame_normalised)
            self.frames_freq_bins.append(frames_freq[frames_freq>0])
            self.frames_phase_angle_bins.append(phase_angle[frames_freq>0])

        #plt.scatter(self.frames_freq_bins[0],self.frames_phase_angle_bins[0])
    def spectral_flux(self):
        self.spectral_flux = []
        for frame_index in range(len(self.frames)):
            test = copy.deepcopy(self.frames_fft_normalised[frame_index])
            test = np.insert(test,len(test),1)
            test_1 = copy.deepcopy(self.frames_fft_normalised[frame_index])
            test_1 = np.insert(test_1,0,1)
            self.spectral_flux.append(np.sum((test - test_1)[1:-1]**2))
        #plt.scatter(np.arange(len(self.frames)),self.spectral_flux)
    def spectral_rolloff(self):
        self.spectral_rolloff = []
        percentage = 0.93
        for frame_index in range(len(self.frames)):
            spectral_cum_sum = np.cumsum(self.frames_fft_normalised[frame_index])
            roll_of_percentage = percentage*spectral_cum_sum[-1]
            lower_spectral_indices = np.argwhere(spectral_cum_sum<roll_of_percentage)
            spectral_roll_off_f = self.frames_freq_bins[frame_index][lower_spectral_indices[-1][0]]
            self.spectral_rolloff.append(spectral_roll_off_f)
        #plt.scatter(np.arange(len(self.frames)),self.spectral_rolloff)
    def spectral_centroid(self):
        self.spectral_centroid = []
        for frame_index in range(len(self.frames)):
            num = np.sum(self.frames_freq_bins[frame_index]*(self.frames_fft_normalised[frame_index]**2))
            den = np.sum(self.frames_fft_normalised[frame_index]**2)
            self.spectral_centroid.append(num/den)
        #plt.scatter(np.arange(len(self.frames)),self.spectral_centroid)
    def bandwidth(self):
        self.bandwidth_ = []
        for frame_index in range(len(self.frames)):
            num = np.sum(((self.frames_freq_bins[frame_index] - self.spectral_centroid[frame_index])**2)*\
                         (self.frames_fft_normalised[frame_index]**2))
            den = np.sum(self.frames_fft_normalised[frame_index]**2)
            self.bandwidth_.append(num/den)
        #plt.scatter(np.arange(len(self.frames)),self.bandwidth_)
    def nwpd(self):
        self.nwpd_list = []
        for frame_index in range(len(self.frames)):
            each_phase = copy.deepcopy(self.frames_phase_angle_bins[frame_index])
            second_phase_deriv = np.diff(each_phase,n = 2)
            nwpd_ = np.sum(self.frames_fft_normalised[frame_index][0:-2]*second_phase_deriv)
            self.nwpd_list.append(nwpd_)
        #plt.scatter(np.arange(len(frames)),nwpd)
    def relative_spectral_entropy(self):
        self.spectral_entropy = []
        for i,frame_index in enumerate(range(len(self.frames))):
            if i == 0:
                m_t_prev = np.zeros(self.frames_fft_normalised[frame_index].shape)
                p_t = copy.deepcopy(self.frames_fft_normalised[frame_index])
                m_t_curr = (m_t_prev * 0.9) + (p_t * 0.1)
            else:
                m_t_prev = copy.deepcopy(m_t_curr)
                p_t = copy.deepcopy(self.frames_fft_normalised[frame_index])
                m_t_curr = (m_t_prev * 0.9) + (p_t * 0.1)
                rse_ = -np.sum(self.frames_fft_normalised[frame_index]*\
                               (np.log(self.frames_fft_normalised[frame_index]) - np.log(m_t_prev)))
                self.spectral_entropy.append(rse_)
    def return_(self):
        return [self.ZCR,self.RMS_count,self.spectral_flux,\
                self.spectral_rolloff,self.spectral_centroid,self.bandwidth_,self.nwpd_list,self.spectral_entropy]