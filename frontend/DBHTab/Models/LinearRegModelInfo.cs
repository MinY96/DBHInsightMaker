using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DBHTab.Models
{
    public class LinearRegModelInfo : RegModelInfo
    {
        #region Field Variables
        #endregion

        #region Initialize

        public LinearRegModelInfo()
        {

        }

        #endregion

        #region Properties

        public double SSE { get; set; } = default!;
        public double SSR { get; set; } = default!;
        public double SST { get; set; } = default!;
        public double RSquare { get; set; } = default!;
        public double RSquareAdj { get; set; } = default!;
        public double MAE { get; set; } = default!;
        public double MSE { get; set; } = default!;
        public double RMSE { get; set; } = default!;
        public double MAPE { get; set; } = default!;
        public double MPE { get; set; } = default!;

        #endregion

        #region Commands

        #endregion

        #region Public Events
        #endregion

        #region Public Methods
        #endregion

        #region Private Methods
        #endregion

        #region Protected Methods
        #endregion
    }
}
