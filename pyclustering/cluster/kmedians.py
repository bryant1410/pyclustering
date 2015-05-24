"""!

@brief Cluster analysis algorithm: K-Medians
@details Based on book description:
         - J.B.MacQueen. Some Methods for Classification and Analysis of Multivariate Observations. 1967.

@authors Andrei Novikov (spb.andr@yandex.ru)
@version 1.0
@date 2014-2015
@copyright GNU Public License

@cond GNU_PUBLIC_LICENSE
    PyClustering is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    PyClustering is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
@endcond

"""


from pyclustering.support import euclidean_distance_sqrt, geometric_median;

class kmedians:
    """!
    @brief Class represents clustering algorithm K-Medians.
    @details The algorithm is less sensitive to outliers tham K-Means.
    
    Example:
    @code
        # load list of points for cluster analysis
        sample = read_sample(path);
        
        # create instance of K-Medians algorithm
        kmedians_instance = kmedians(sample, [ [0.0, 0.1], [2.5, 2.6] ]);
        
        # run cluster analysis and obtain results
        kmedians_instance.process();
        kmedians_instance.get_clusters();    
    @endcode
    
    """
    __pointer_data = None;
    __clusters = None;
    __medians = None;
    __tolerance = 0.0;
    
    
    def __init__(self, data, initial_centers, tolerance = 0.25):
        """!
        @brief Constructor of clustering algorithm K-Medians.
        
        @param[in] data (list): Input data that is presented as list of points (objects), each point should be represented by list or tuple.
        @param[in] initial_centers (list): Initial coordinates of centers of clusters that are represented by list: [center1, center2, ...].
        @param[in] tolerance (double): Stop condition: if maximum value of change of centers of clusters is less than tolerance than algorithm will stop processing
        
        """
        self.__pointer_data = data;
        self.__clusters = [];
        self.__medians = initial_centers[:];     # initial centers shouldn't be chaged
        self.__tolerance = tolerance;


    def process(self):
        """!
        @brief Performs cluster analysis in line with rules of K-Medians algorithm.
        
        @remark Results of clustering can be obtained using corresponding get methods.
        
        @see get_clusters()
        @see get_centers()
        
        """
        
        changes = float('inf');
         
        stop_condition = self.__tolerance * self.__tolerance;   # Fast solution
        #stop_condition = self.__tolerance;              # Slow solution
         
        # Check for dimension
        if (len(self.__pointer_data[0]) != len(self.__medians[0])):
            raise NameError('Dimension of the input data and dimension of the initial cluster medians must be equal.');
         
        while (changes > stop_condition):
            self.__clusters = self.__update_clusters();
            updated_centers = self.__update_medians();  # changes should be calculated before asignment
         
            changes = max([euclidean_distance_sqrt(self.__medians[index], updated_centers[index]) for index in range(len(self.__medians))]);    # Fast solution
             
            self.__medians = updated_centers;


    def get_clusters(self):
        """!
        @brief Returns list of allocated clusters, each cluster contains indexes of objects in list of data.
        
        @see process()
        @see get_centers()
        
        """
        
        return self.__clusters;
    
    
    def get_centers(self):
        """!
        @brief Returns list of centers of allocated clusters.
        
        @see process()
        @see get_clusters()
        
        """

        return self.__medians;


    def __update_clusters(self):
        """!
        @brief Calculate Manhattan distance to each point from the each cluster. 
        @details Nearest points are captured by according clusters and as a result clusters are updated.
        
        @return (list) updated clusters as list of clusters where each cluster contains indexes of objects from data.
        
        """
        
        clusters = [[] for i in range(len(self.__medians))];
        for index_point in range(len(self.__pointer_data)):
            index_optim = -1;
            dist_optim = 0.0;
             
            for index in range(len(self.__medians)):
                dist = euclidean_distance_sqrt(self.__pointer_data[index_point], self.__medians[index]);
                 
                if ( (dist < dist_optim) or (index is 0)):
                    index_optim = index;
                    dist_optim = dist;
             
            clusters[index_optim].append(index_point);
             
        return clusters;
    
    
    def __update_medians(self):
        """!
        @brief Calculate medians of clusters in line with contained objects.
        
        @return (list) list of medians for current number of clusters.
        
        """
         
        medians = [[] for i in range(len(self.__clusters))];
         
        for index in range(len(self.__clusters)):
            meadian_index = geometric_median(self.__pointer_data, self.__clusters[index]);
            medians[index] = self.__pointer_data[meadian_index];
             
        return medians;