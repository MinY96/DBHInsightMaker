using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DBHTab.Models
{
    public class LogisticRegModelInfo : RegModelInfo
    {
        #region Field Variables
        #endregion

        #region Initialize

        public LogisticRegModelInfo()
        {

        }

        #endregion

        #region Properties

        public ClassificationMetrics ROCMetrics { get; set; }
        public ClassificationMetrics PRMetrics { get; set; }

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
